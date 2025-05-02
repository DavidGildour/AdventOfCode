// https://adventofcode.com/2024/day/10
package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"regexp"
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

type Dir int

const (
	N Dir = iota
	E
	S
	W
)

const (
	STARTING_POINT = '0'
	ENDING_POINT   = '9'
	VOID           = '\000'
)

type Grid struct {
	Data      string
	RowLength int
	ColLength int
}

func (g Grid) GetValueIfExists(pos Position) byte {
	if g.PositionExists(pos) {
		return g.GetValue(pos)
	}

	return byte(VOID)
}

func (g Grid) GetValue(pos Position) byte {
	return g.Data[pos.ToIndex(g.RowLength)]
}

func (g Grid) PositionExists(pos Position) bool {
	return pos.X >= 0 && pos.X < g.RowLength && pos.Y >= 0 && pos.Y < g.ColLength
}

func (g Grid) get2DPositions(ch rune, offset int) (positions []Position) {
	ix := strings.IndexRune(g.Data[offset:], ch)
	if ix >= 0 {
		adjustedIx := ix + offset
		position := createPositionFromIndex(adjustedIx, g.RowLength)
		positions = append(positions, position)
		return append(positions, g.get2DPositions(ch, adjustedIx+1)...)
	}

	return
}

func (g Grid) GetStartingPoints() (res []Position) {
	return g.get2DPositions(STARTING_POINT, 0)
}

func (g Grid) Walk(p Position, currentValue byte) []Position {
	if currentValue == ENDING_POINT {
		return []Position{p}
	}

	var candidates []Position
	nextValue := currentValue + 1
	for _, dir := range [4]Dir{N, E, W, S} {
		neighbour := p.GetNeighbour(dir)
		if g.GetValueIfExists(neighbour) == nextValue {
			candidates = append(candidates, g.Walk(neighbour, nextValue)...)
		}
	}

	return candidates
}

func (g Grid) FindTrailheadScore(start Position) (score int) {
	visitedPos := make(map[Position]bool)
	for _, pos := range g.Walk(start, STARTING_POINT) {
		visitedPos[pos] = true
	}

	for range visitedPos {
		score++
	}

	return
}

func (g Grid) FindTrailheadRating(start Position) (score int) {
	for range g.Walk(start, STARTING_POINT) {
		score++
	}

	return
}

func (g Grid) String() string {
	var builder strings.Builder
	for i, ch := range g.Data {
		if i > 0 && i%g.RowLength == 0 {
			builder.WriteRune('\n')
		}
		builder.WriteRune(ch)
	}

	return builder.String()
}

func createGridFromString(dataString string) Grid {
	rowLength := strings.Index(dataString, "\n")
	colLength := strings.Count(dataString, "\n") + 1

	re := regexp.MustCompile(`\s`)

	return Grid{
		Data:      re.ReplaceAllString(dataString, ""),
		RowLength: rowLength,
		ColLength: colLength,
	}
}

type Position struct {
	X int
	Y int
}

func (p Position) ToIndex(rowLength int) int {
	return (p.Y * rowLength) + p.X
}

func (p Position) GetNeighbour(dir Dir) Position {
	switch dir {
	case N:
		return Position{p.X, p.Y - 1}
	case E:
		return Position{p.X + 1, p.Y}
	case S:
		return Position{p.X, p.Y + 1}
	case W:
		return Position{p.X - 1, p.Y}
	default:
		panic(fmt.Sprintf("Invalid direction: %v", dir))
	}
}

func createPositionFromIndex(ix, rowLength int) Position {
	return Position{
		X: ix % rowLength,
		Y: ix / rowLength,
	}
}

type DirectedPosition struct {
	Pos Position
	Dir Dir
}

func partOne(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part one")

	grid := createGridFromString(dataString)
	for _, s := range grid.GetStartingPoints() {
		result += grid.FindTrailheadScore(s)
	}

	return
}

func partTwo(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part two")

	grid := createGridFromString(dataString)
	for _, s := range grid.GetStartingPoints() {
		result += grid.FindTrailheadRating(s)
	}

	return
}

func main() {
	flag.Parse()

	var inputFile string
	if *isTest {
		inputFile = "input_test.txt"
		fmt.Println("Running 2024/10 solution on test input.")
	} else {
		inputFile = "input.txt"
		fmt.Println("Running 2024/10 solution on full input.")
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
