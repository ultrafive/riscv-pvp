SUBDIRS := $(wildcard */*/*/)
  
all clean: $(SUBDIRS)

$(SUBDIRS):
	@$(MAKE) -C $@ $(MAKECMDGOALS) >$@/test.log 2>&1
	@[ "$(V)" != 1 ] || echo "$@ done."

.PHONY: all clean $(SUBDIRS)