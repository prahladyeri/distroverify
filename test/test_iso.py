from distroverify import main
import os

def test_fake_iso():
	for file in os.scandir(r"test"):
		a = os.path.splitext(file.path)
		if a[1] == '.iso': 
			result = main.main([file.path])
			assert result == False or result == None
			
