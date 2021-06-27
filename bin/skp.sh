#!/bin/bash

eval "$(direnv hook bash)"

#echo $@
invoke -e -r $JUPYTER_HOME/src/tasks "$@"
