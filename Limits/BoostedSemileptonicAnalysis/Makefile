ROOTCFLAGS   := $(shell root-config --cflags)  -I/uscmst1/prod/sw/cms/slc5_amd64_gcc462/lcg/roofit/5.32.03-cms15/include
ROOTLDFLAGS  := $(shell root-config --ldflags) -L/uscmst1/prod/sw/cms/slc5_amd64_gcc462/lcg/roofit/5.32.03-cms15/lib
ROOTLIBS     := $(shell root-config --libs)

CXXFLAGS     := -g -Wall -fPIC $(ROOTCFLAGS)

LIBS := $(ROOTLIBS) -lm -lRooFit -lRooFitCore -lFoam -lMinuit -lMathMore

%: %.cxx
	@echo -n "Compiling $< ..."
	$(CXX) $(CXXFLAGS) $< $(ROOTLDFLAGS) $(LIBS) -o $@
	@echo "Done"
