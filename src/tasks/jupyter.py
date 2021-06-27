from invoke import task
import os, sys, re
import skp_env, skp_util

def download_package(c, url, pname):
    fname = url.split('/')[-1]
    cmd = f"wget -q {url} -O {skp_env.JUPYTER_HOME}/usr/{fname}" # 출력이 길다면, -q 옵션 사용 가능
    skp_util.run_with_exit(c, cmd)
    cmd = f"cd {skp_env.JUPYTER_HOME}/usr && mv ./{pname} ./{pname}-$(date +'%Y%m%dT%H%m%S') && mkdir ./{pname} && tar -zxf {fname} -C {pname} --strip-components=1"
    skp_util.run_with_exit(c, cmd)

@task
def install(c):
    skp_util.mkdir_usr(c, f"{skp_env.JUPYTER_HOME}")

    # Common
    if skp_util.is_macos(c):
        cmd = "brew update"
        skp_util.run_with_exit(c, cmd)
    if skp_util.is_ubuntu(c):
        cmd = "sudo apt-get update"
        skp_util.run_with_exit(c, cmd)
        cmd = f"sudo apt-get install -y build-essential vim curl wget git git-flow cmake bzip2 sudo unzip net-tools libffi-dev libssl-dev zlib1g-dev libbz2-dev libreadline-dev sqlite3 libsqlite3-dev llvm libfreetype6-dev libxft-dev libcurl4-gnutls-dev libxml2-dev texlive-xetex "
        skp_util.run_with_exit(c, cmd)
        cmd = f"sudo apt-get install -y software-properties-common libjpeg-dev libpng-dev ncurses-dev imagemagick libgraphicsmagick1-dev libzmq3-dev gfortran gnuplot gnuplot-x11 libsdl2-dev openssh-client htop iputils-ping "
        skp_util.run_with_exit(c, cmd)
        cmd = f"sudo apt-get install -y freetds-bin ldap-utils libsasl2-2 libsasl2-modules libssl1.1 locales lsb-release sasl2-bin unixodbc "
        skp_util.run_with_exit(c, cmd)

    # Jupyter Lab
    cmd = "pip install jupyterlab"
    skp_util.run_with_exit(c, cmd)

    # JAVA
    if skp_util.is_macos(c):
        cmd = "brew tap AdoptOpenJDK/openjdk"
        skp_util.run_with_exit(c, cmd)
        cmd = f"brew install --cask {skp_env.JAVA_VER}"
        skp_util.run_with_exit(c, cmd)
    if skp_util.is_ubuntu(c):
        cmd = f"sudo apt install -y {skp_env.JAVA_VER}"
        skp_util.run_with_exit(c, cmd)

    # SCALA
    url = f"https://downloads.lightbend.com/scala/{skp_env.SCALA_VER}/scala-{skp_env.SCALA_VER}.tgz"
    download_package(c, url, f"scala-{skp_env.SCALA_VER}")

    # JULIA
    url = f"https://julialang-s3.julialang.org/bin/linux/x64/{skp_env.JULIA_VER.rpartition('.')[0]}/julia-{skp_env.JULIA_VER}-linux-x86_64.tar.gz"
    download_package(c, url, f"julia-{skp_env.JULIA_VER}")
    cmd = "julia -e 'using Pkg;Pkg.update()'"
    skp_util.run_with_exit(c, cmd)

    # R
    if skp_util.is_macos(c):
        pass
    if skp_util.is_ubuntu(c):
        cmd = "sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9"
        skp_util.run_with_exit(c, cmd)
        cmd = f"sudo add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu {skp_util.get_ubuntu_codename(c)}-cran40/'"
        skp_util.run_with_exit(c, cmd)
        cmd = "sudo apt-get update"
        skp_util.run_with_exit(c, cmd)
        cmd = "sudo apt-get --allow-unauthenticated install -y --no-install-recommends r-base r-base-dev"
        skp_util.run_with_exit(c, cmd)

    # PySpark
    cmd = f"pip install pyspark[sql]=={skp_env.SPARK_VER}"
    skp_util.run_with_exit(c, cmd)

    # Jupyter Kernel - Scala 
    cmd = "pip install spylon-kernel"
    skp_util.run_with_exit(c, cmd)

    # Jupyter Kernel - R
    cmd = f"mkdir -p {skp_env.R_LIBS}"
    skp_util.run_with_exit(c, cmd)
    cmd = '''R -e "install.packages(c('curl', 'repr', 'httr'), repos='http://cran.rstudio.com/')"'''
    skp_util.run_with_exit(c, cmd)
    cmd = '''R -e "install.packages(c('devtools'), repos='http://cran.rstudio.com/')"'''
    skp_util.run_with_exit(c, cmd)
    cmd = '''R -e "install.packages(c('pbdZMQ', 'IRdisplay', 'evaluate', 'crayon', 'uuid', 'digest'), repos='http://cran.rstudio.com/')"'''
    skp_util.run_with_exit(c, cmd)
    cmd = '''R -e "install.packages(c('SparkR'), repos='http://cran.rstudio.com/')"'''
    skp_util.run_with_exit(c, cmd)
    cmd = '''R -e "install.packages(c('IRkernel'), repos='http://cran.rstudio.com/')"'''
    skp_util.run_with_exit(c, cmd)
    cmd = '''R -e "IRkernel::installspec()"'''
    skp_util.run_with_exit(c, cmd)

    # Jupyter Kernel - Julia
    cmd = """julia -e 'using Pkg;Pkg.add("IJulia")'"""
    skp_util.run_with_exit(c, cmd)
    cmd = """julia -e 'using IJulia'"""
    skp_util.run_with_exit(c, cmd)

    # PIP Packages
    if "TRUE" in skp_env.JUPYTER_GPU:
        cmd = f"pip install -r {skp_env.JUPYTER_HOME}/etc/requirements_gpu.txt"
    else:
        cmd = f"pip install -r {skp_env.JUPYTER_HOME}/etc/requirements_cpu.txt"
    skp_util.run_with_exit(c, cmd)

@task
def install_pip(c):
    if "TRUE" in skp_env.JUPYTER_GPU:
        cmd = f"pip install -r {skp_env.JUPYTER_HOME}/etc/requirements_gpu.txt"
    else:
        cmd = f"pip install -r {skp_env.JUPYTER_HOME}/etc/requirements_cpu.txt"
    skp_util.run_with_exit(c, cmd)

@task
def start(c):
    cmd = f"envsubst < {skp_env.JUPYTER_HOME}/etc/pm2.json | pm2 start -"
    skp_util.run_with_exit(c, cmd)

@task
def stop(c):
    cmd = f"envsubst < {skp_env.JUPYTER_HOME}/etc/pm2.json | pm2 stop -"
    skp_util.run_with_exit(c, cmd)
    cmd = f"envsubst < {skp_env.JUPYTER_HOME}/etc/pm2.json | pm2 delete -"
    skp_util.run_with_exit(c, cmd)

@task
def restart(c):
    stop(c)
    start(c)
