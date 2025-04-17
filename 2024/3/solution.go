// https://adventofcode.com/2024/day/3
package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
	"time"
)


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

func multiplyMatchNums(matchGroup []string) (int, error) {
	a, errA := strconv.Atoi(matchGroup[1])
	b, errB := strconv.Atoi(matchGroup[2])

	if errA != nil {
		return 0, errA
	}
	if errB != nil {
		return 0, errB
	}

	return a * b, nil
}


func partOne(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part one")

	re := regexp.MustCompile(`mul\((\d{1,3}),(\d{1,3})\)`)
	matches := re.FindAllStringSubmatch(dataString, -1)
	for _, matchGroup := range matches {
		mult, err := multiplyMatchNums(matchGroup)
		if err != nil {
			return 0, err
		}

		result += mult
	}
	return
}


func partTwo(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part one")

	re := regexp.MustCompile(`mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)`)
	matches := re.FindAllStringSubmatch(dataString, -1)
	enabled := true
	for _, matchGroup := range matches {
		switch matchGroup[0] {
		case "do()":
			enabled = true
		case "don't()":
			enabled = false
		default:
			if enabled {
				mult, err := multiplyMatchNums(matchGroup)
				if err != nil {
					return 0, err
				}

				result += mult
			}
		}
	}

	return
}


func main() {
	flag.Parse()
	
	var inputFile string
	if *isTest {
		inputFile = "input_test.txt"
		fmt.Println("Running 2024/3 solution on test input.")
	} else {
		inputFile = "input.txt"
		fmt.Println("Running 2024/3 solution on full input.")
	}

	data, err := getFileInput(inputFile)
	if err != nil {
		fmt.Printf("Error reading file:\n> %v", err)
		return
	}

	partOneSolution, err := partOne(data)
	if err != nil {
		fmt.Printf("Error solving part one:\n> %v", err)
		return
	}
	fmt.Printf("Part 1: %v\n", partOneSolution)

	partTwoSolution, err := partTwo(data)
	if err != nil {
		fmt.Printf("Error solving part two:\n> %v", err)
		return
	}

	fmt.Printf("Part 2: %v\n", partTwoSolution)
}
