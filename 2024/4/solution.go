// https://adventofcode.com/2024/day/4
package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"strings"
	"sync"
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

type Position struct {
	x int
	y int
}

type Dir int

const (
	N Dir = iota
	E
	W
	S
)

func (p Position) toIndex(rowLength int) int {
	return p.x*rowLength + p.y
}

func createPositionFromIndex(ix, rowLength int) Position {
	return Position{
		x: ix % rowLength,
		y: ix / rowLength,
	}
}

func get2DPositions(str string, ch rune, rowLength, offset int) (positions []Position) {
	ix := strings.IndexRune(str, ch)
	if ix >= 0 {
		adjustedIx := ix + offset
		position := createPositionFromIndex(adjustedIx, rowLength)
		positions = append(positions, position)
		return append(positions, get2DPositions(str[ix+1:], ch, rowLength, adjustedIx+1)...)
	}

	return
}

func partOne(dataString string) (result string, err error) {
	defer timeTrack(time.Now(), "part one")

	// need to add 1 to adjust for '\n'
	rowLength := strings.Index(dataString, "\n") + 1
	positions := get2DPositions(dataString, 'X', rowLength, 0)

	var wg sync.WaitGroup
	wg.Add(len(positions))

	for _, pos := range positions {
		go func() {
			wg.Add(1)
		}()
	}

	fmt.Println(rowLength, positions)

	return
}

func partTwo(dataString string) (result string, err error) {
	defer timeTrack(time.Now(), "part two")
	return
}

func main() {
	flag.Parse()

	var inputFile string
	if *isTest {
		inputFile = "input_test.txt"
		fmt.Println("Running 2024/4 solution on test input.")
	} else {
		inputFile = "input.txt"
		fmt.Println("Running 2024/4 solution on full input.")
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
