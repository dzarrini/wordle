# Compiler to use
CXX = g++

# Compiler flags
CXXFLAGS = -std=c++20 -Wall -Wextra -pedantic -O3

# Target executable name
TARGET = wordle_binary

# Source files
SRC = main.cpp

# Object files
OBJ = $(SRC:.cpp=.o)

# Default target to compile the program
all: $(TARGET)

# Rule to link the object files and create the executable
$(TARGET): $(OBJ)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJ)

# Rule to compile the source files into object files
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean up build files
clean:
	rm -f $(OBJ) $(TARGET)

# Run the executable
run: $(TARGET)
	./$(TARGET)

# Phony targets
.PHONY: all clean run
