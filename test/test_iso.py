from distroverify import distroverify
import os

def test_fake_iso():
	for file in os.scandir("test/fake_iso"):
		a = os.path.splitext(file.path)
		if a[1] == '.iso': 
			result = distroverify.main([file.path])
			assert result == False or result == None
			
