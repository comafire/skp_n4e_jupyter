from invoke import Collection
import skp_env, skp_util

ns = Collection()

if skp_env.JUPYTER:
    import jupyter
    ns.add_collection(Collection.from_module(jupyter), 'jupyter')
