 ifeq (, $(shell which pip3))
 ifeq (, $(shell which pip))
 $(error "No pip or pip3 in $(PATH)")
 else
 use_pip := pip
 $(warning "No pip3 in $(PATH). Using python2/pip installation,
  but note that program is not tested for python 2")
 endif
 else
 use_pip := pip3
 endif

install:
	${use_pip} install -r requirements.txt