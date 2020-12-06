# Minimal makefile for Sphinx documentation
#
export SPHINX_APIDOC_OPTIONS=members,no-undoc-members,no-show-inheritance

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)



buildapi:
	sphinx-apidoc -fMeET -o source/_modules ../qt_material

	#mkdir -p source/_notebooks/images

	#cp ../notebooks/*.ipynb source/_notebooks/
	#cp ../notebooks/images/* source/_notebooks/images

	#rm source/_notebooks/*.rst
	#rm source/_notebooks/SANDBOX.ipynb
	#jupyter nbconvert --to rst source/_notebooks/*.ipynb
	#rm source/_notebooks/*.ipynb


	cp source/index.rst ../README.rst

