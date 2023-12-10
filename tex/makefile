.PHONY: build
build: 
	pdflatex -shell-escape report.tex


.PHONY: build_bib
build_bib:
	biber report


.PHONY: move
move:
	-mkdir ../pdf           
	-mv report.pdf ../pdf
	-mkdir ../out        
	-mv *.aux *.log *.bbl *.blg *.dvi *.out *.toc *.bcf *.xml *.fdb_latexmk *.fls *.gz ../out