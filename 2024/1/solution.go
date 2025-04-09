package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"
	"sync"
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

	dataString := string(rawData)

	return dataString, nil
}

func getLocationSlices(dataString string) (left, right []int, err error) {
	for line := range strings.SplitSeq(dataString, "\n") {
		if line != "" {
			numbers := strings.Fields(line)

			leftLoc, errLeft := strconv.Atoi(numbers[0])
			rightLoc, errRight := strconv.Atoi(numbers[1])
			if errLeft != nil {
				return nil, nil, errLeft
			}
			left = append(left, leftLoc)

			if errRight != nil {
				return nil, nil, errRight
			}
			right = append(right, rightLoc)
		}
	}

	return
}

func absDiff(a, b int) int {
    if a > b {
        return a - b
    }
    return b - a
}

func count(value int, arr []int, c chan int) {
	var counter int
	for _, x := range arr {
		if x == value { counter++ }
	}
	c <- value * counter
} 

func partOne(dataString string) (sum int, err error) {
	defer timeTrack(time.Now(), "part one")

	left, right, err := getLocationSlices(dataString)
	if err != nil {
		return 0, err
	}
	
	sort.Ints(left)
	sort.Ints(right)

	for i := range left {
		sum += absDiff(left[i], right[i])
	}

	return
}

func partTwo(dataString string) (sum int, err error) {
	defer timeTrack(time.Now(), "part two")

	left, right, err := getLocationSlices(dataString)
	if err != nil {
		return 0, err
	}

	var wg sync.WaitGroup
	sumChan := make(chan int, len(left))
	for _, value := range left {
		wg.Add(1)
		go func() {
			defer wg.Done()
			count(value, right, sumChan)
		}()
	}

	go func() {
		wg.Wait()
		close(sumChan)
	}()

	for value := range sumChan {
		sum += value
	} 

	return
}



func main() {
	flag.Parse()
	
	var inputFile string
	if *isTest {
		inputFile = "input_test.txt"
	} else {
		inputFile = "input.txt"
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