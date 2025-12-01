// https://adventofcode.com/2025/day/1
package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"time"
)


// #####################  <UTILS> #####################

var isTest *bool = flag.Bool("test", false, "Read the test input")


func timeTrack(start time.Time, name string) {
    elapsed := time.Since(start)
    log.Printf("%s took %s", name, elapsed)
}


func getFileInput(inputFile string) (string, error) {
	rawData, err := os.ReadFile(inputFile)
	if err != nil {
		return "", err
	}

	return string(rawData), nil
}

// ##################### </UTILS> #####################


func partOne(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part one")
	return
}


func partTwo(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part two")
	return
}


func main() {
	flag.Parse()
	
	var inputFile string
	if *isTest {
		inputFile = "input_test.txt"
		fmt.Println("Running 2025/1 solution on test input.")
	} else {
		inputFile = "input.txt"
		fmt.Println("Running 2025/1 solution on full input.")
	}

	data, err := getFileInput(inputFile)
	if err != nil {
		fmt.Printf("Error reading file:\n> %v", err)
		return
	}

	partOneSolution, err := partOne(data)
	if err != nil {
		fmt.Printf("Error solving part one:\n> %v\n", err)
		return
	}
	fmt.Printf("Part 1: %v\n", partOneSolution)

	partTwoSolution, err := partTwo(data)
	if err != nil {
		fmt.Printf("Error solving part two:\n> %v\n", err)
		return
	}

	fmt.Printf("Part 2: %v\n", partTwoSolution)
}
