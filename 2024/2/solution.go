// https://adventofcode.com/2024/day/2
package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
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

func sign(x int) int {
	if x < 0 {
		return -1
	} else if x > 0 {
		return 1
	}
	return 0
}

func checkAgainstDir(diff int, dir *int) bool {
	if diff == 0 {
		return false
	}

	dirDetermined := ((*dir) != 0)
	if !dirDetermined {
		*dir = sign(diff)
	}

	return (*dir)*diff < 0 || diff*diff > 9
}

func reportIsSafe(report []int) bool {
	var changeDir int
	for i := range len(report) - 1 {
		diff := report[i+1] - report[i]
		if !checkAgainstDir(diff, &changeDir) {
			return false
		}
	}
	return true
}

func parseReport(repStr string) (res []int, err error) {
	for _, s := range strings.Fields(repStr) {
		num, err := strconv.Atoi(s)
		if err != nil {
			return nil, err
		}
		res = append(res, num)
	}
	return
}

func parseReports(reportStrings []string) (result [][]int, err error) {
	for _, repStr := range reportStrings {
		intRep, err := parseReport(repStr)
		if err != nil {
			return nil, err
		}
		result = append(result, intRep)
	}

	return
}

func partOne(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part one")

	strReports := strings.Split(dataString, "\n")
	intReports, err := parseReports(strReports)

	if err != nil {
		return 0, err
	}

	for _, rep := range intReports {
		if reportIsSafe(rep) {
			result++
		}
	}

	return
}

func partTwo(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part one")

	strReports := strings.Split(dataString, "\n")
	intReports, err := parseReports(strReports)

	if err != nil {
		return 0, err
	}

	for _, rep := range intReports {
		if reportIsSafe(rep) {
			result++
		} else {
			// TO DO
		}
	}

	return
}

func main() {
	flag.Parse()

	var inputFile string
	if *isTest {
		inputFile = "input_test.txt"
		fmt.Println("Running 2024/2 solution on test input.")
	} else {
		inputFile = "input.txt"
		fmt.Println("Running 2024/2 solution on full input.")
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
