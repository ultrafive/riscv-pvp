SIMS += spike

.NOTPARALLEL:
spike: spike.clean spike.log spike.sig

spike.run: test.elf
	$(SPIKE) $(SPIKE_OPTS) +signature=spike.sig $< >spike.tmp 2>&1 && touch $@

spike.log: spike.run
	mv -f spike.tmp $@
	touch $@
spike.sig: spike.run
	touch $@

spike.clean:
	@rm -f spike.run

