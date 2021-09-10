SIMS += vcs

.NOTPARALLEL:
vcs: vcs.clean vcs.log vcs.sig


ifeq ($(tsiloadmem),True)
    opt_ldmem := +loadmem=test.hex +loadmem_addr=80000000 +max-cycles=$(vcstimeout)
else
    opt_ldmem := +max-cycles=$(vcstimeout)
endif

ifeq ($(fsdb),True)
	opt_fsdb := +fsdbfile=test.fsdb
else
	opt_fsdb := 
endif

ifeq ($(lsf),True)
	lsf_cmd := $(LSF_CMD)
else
	lsf_cmd := 
endif

vcs_opts := +permissive $(opt_fsdb) $(opt_ldmem) +permissive-off +signature=vcs.sig +signature-granularity=32
	
vcs.run: test.elf
	smartelf2hex.sh $< > test.hex
	$(lsf_cmd) $(VCS) $(vcs_opts) $< >vcs.tmp 2>&1 && touch $@
	@stty sane

vcs.clean:
	@rm -f vcs.run

vcs.log: vcs.run
	@mv -f vcs.tmp $@
	@touch $@
vcs.sig: vcs.run
	@touch $@

