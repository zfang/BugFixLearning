all: Mono.Cecil.dll bin 

Mono.Cecil.dll: 
	cp `pkg-config --variable=Libraries cecil` .

bin:
	gmcs dotnetclassextract.cs -r:Mono.Cecil.dll

.PHONY: all
