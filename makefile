.PHONY: open
open:
	open pdf/report.pdf


.PHONY: clean
clean:
	-mkdir out        
	-mv ./tex/*.aux ./tex/*.log ./tex/*.bbl ./tex/*.blg ./tex/*.dvi ./tex/*.out ./tex/*.toc ./tex/*.bcf ./tex/*.xml ./tex/*.fdb_latexmk ./tex/*.fls ./tex/*.gz out
	-rm -rf pdf out

.PHONY: save
save:
	-mkdir doc 
	cp ./tex/report.pdf ./doc


.PHONY: run
run:
	make -C tex build
	make -C tex build_bib 
	make -C tex build
	make -C tex move 

.PHONY: drawio
drawio:
	cd tex/inc && draw.io -x -f pdf --crop -p 0 -o img/l.pdf  lab_01_schema.drawio
	cd tex/inc && draw.io -x -f pdf --crop -p 1 -o img/dl.pdf lab_01_schema.drawio
	cd tex/inc && draw.io -x -f pdf --crop -p 2 -o img/rdl.pdf lab_01_schema.drawio
	cd tex/inc && draw.io -x -f pdf --crop -p 3 -o img/rdl_cache.pdf lab_01_schema.drawio

.PHONY: run_prog
run_prog:
	make -C src run
