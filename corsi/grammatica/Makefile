GPQ_THEME=/home/chiara/spinoza

MTEXINPUTS=${GPQ_THEME}:${TEXINPUTS}
MBSTINPUTS=${GPQ_THEME}:${BSTINPUTS}
MBIBINPUTS=${GPQ_THEME}:${BIBINPUTS}

build: 01-article 01-slides

01-article: 01.tempi.article.pdf

01-slides:  01.tempi.slides.pdf

01.tempi.slides.tex: 01.tempi.tex
	echo '\documentclass{presentazioni}' > 01.tempi.slides.tex
	echo >> 01.tempi.slides.tex
	echo '\input{01.tempi}' >> 01.tempi.slides.tex

01.tempi.article.tex: 01.tempi.tex
	echo '\documentclass{presarticle}' > 01.tempi.article.tex
	echo '\setjobnamebeamerversion{01.tempi.slides}' >> 01.tempi.article.tex
	echo '\input{01.tempi}' >> 01.tempi.article.tex

01.tempi.slides.pdf: 01.tempi.tex 01.tempi.slides.tex \
	${GPQ_THEME}/presentazioni.cls \
	beamercolorthemeWD.sty \
	beamerfontthemeWD.sty \
	beamerthemeWD.sty 
	TEXINPUTS=${MTEXINPUTS} BSTINPUTS=${MBSTINPUTS} BIBINPUTS=${MBIBINPUTS} xelatex 01.tempi.slides
	TEXINPUTS=${MTEXINPUTS} BSTINPUTS=${MBSTINPUTS} BIBINPUTS=${MBIBINPUTS} xelatex 01.tempi.slides

01.tempi.article.pdf: 01.tempi.bib 01.tempi.tex 01.tempi.article.tex 01.tempi.slides.pdf \
	${GPQ_THEME}/presarticle.cls \
	beamercolorthemeWD.sty \
	beamerfontthemeWD.sty \
	beamerthemeWD.sty 
	TEXINPUTS=${MTEXINPUTS} BSTINPUTS=${MBSTINPUTS} BIBINPUTS=${MBIBINPUTS} pdflatex 01.tempi.article
	TEXINPUTS=${MTEXINPUTS} BSTINPUTS=${MBSTINPUTS} BIBINPUTS=${MBIBINPUTS} bibtex   01.tempi.article1
	TEXINPUTS=${MTEXINPUTS} BSTINPUTS=${MBSTINPUTS} BIBINPUTS=${MBIBINPUTS} pdflatex 01.tempi.article
	TEXINPUTS=${MTEXINPUTS} BSTINPUTS=${MBSTINPUTS} BIBINPUTS=${MBIBINPUTS} pdflatex 01.tempi.article
