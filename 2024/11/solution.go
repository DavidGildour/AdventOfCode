// https://adventofcode.com/2024/day/11
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

type StoneState struct {
	Stone     string
	IterCount int
}

type StoneCache map[StoneState]int

func (c *StoneCache) Add(stone string, iterCount, val int) {
	(*c)[StoneState{stone, iterCount}] = val
}

func (c *StoneCache) Read(stone string, iterCount int) (int, bool) {
	v, ok := (*c)[StoneState{stone, iterCount}]
	return v, ok
}

var Cache StoneCache = make(StoneCache)
var DebugStates [][]string

func MustAtoi(s string) int {
	i, err := strconv.Atoi(s)
	if err != nil {
		panic("WTF")
	}

	return i
}

func ParseInitialStones(data string) []string {
	return strings.Fields(data)
}

func NormalizeStone(stone string) string {
	next := strings.TrimLeft(stone, "0")

	if next == "" {
		return "0"
	}
	return next
}

func StoneExpansion(stone string, depth, targetDepth int) int {
	if depth == targetDepth {
		return 1
	}

	iterCount := targetDepth - depth
	cachedValue, ok := Cache.Read(stone, iterCount)
	if ok {
		return cachedValue
	}

	var result int
	if stone == "0" {
		result = StoneExpansion("1", depth+1, targetDepth)
		Cache.Add(stone, iterCount, result)
	} else if digitCount := len(stone); digitCount%2 == 0 {
		stoneA := stone[:digitCount/2]
		stoneB := NormalizeStone(stone[digitCount/2:])
		result = StoneExpansion(stoneA, depth+1, targetDepth) + StoneExpansion(stoneB, depth+1, targetDepth)

		Cache.Add(stone, iterCount, result)
	} else {
		result = StoneExpansion(strconv.Itoa(MustAtoi(stone)*2024), depth+1, targetDepth)
		Cache.Add(stone, iterCount, result)
	}

	return result
}

func CountStonesAfterBlinks(stones []string, blinkCount int) (res int) {
	for _, stone := range stones {
		res += StoneExpansion(stone, 0, blinkCount)
	}

	return res
}

func partOne(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part one")

	stones := ParseInitialStones(dataString)
	return CountStonesAfterBlinks(stones, 25), nil
}

func partTwo(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part two")

	stones := ParseInitialStones(dataString)
	return CountStonesAfterBlinks(stones, 75), nil
}

func main() {
	flag.Parse()

	var inputFile string
	if *isTest {
		inputFile = "input_test.txt"
		fmt.Println("Running 2024/11 solution on test input.")
	} else {
		inputFile = "input.txt"
		fmt.Println("Running 2024/11 solution on full input.")
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
