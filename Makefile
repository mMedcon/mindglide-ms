setup:
	conda env create -f environment.yml || conda env update -f environment.yml
	@echo 'Environment setup complete. Run: conda activate medon'

clean:
	find . -type d -name '__pycache__' -exec rm -r {} +

