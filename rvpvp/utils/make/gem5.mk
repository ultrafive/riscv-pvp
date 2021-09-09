SIMS += gem5

.NOTPARALLEL:
gem5: gem5.log gem5.sig

gem5.run: test.elf
	$(GEM5) $(GEM5_OPTS) --signature=gem5.sig --kernel=$< >gem5.tmp 2>&1 && touch $@

gem5.clean:
	@rm -f gem5.run

gem5.log: gem5.run
	@mv -f gem5.tmp $@
	@touch $@
gem5.sig: gem5.run
	@touch $@

