// https://adventofcode.com/2024/day/8
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

type Grid struct {
	Data      string
	RowLength int
	ColLength int
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

func (g Grid) GetAntennas() map[rune][]Position {
	antennas := make(map[rune][]Position)

	for i, ch := range g.Data {
		if ch != '.' {
			antennas[ch] = append(antennas[ch], createPositionFromIndex(i, g.RowLength))
		}
	}

	return antennas
}

func createGridFromString(dataString string) Grid {
	rowLength := strings.Index(dataString, "\n") - 1
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

func createPositionFromIndex(ix, rowLength int) Position {
	return Position{
		X: ix % rowLength,
		Y: ix / rowLength,
	}
}

func GetAllAntinodes(p1, p2 Position, grid Grid) []Position {
	antinodes := []Position{p1, p2}

	diffX := p1.X - p2.X
	diffY := p1.Y - p2.Y
	i := 1
	aDone := false
	bDone := false

	for !aDone || !bDone {
		a1 := Position{X: p1.X + diffX * i, Y: p1.Y + diffY * i}
		a2 := Position{X: p2.X - diffX * i, Y: p2.Y - diffY * i}
		if !aDone && grid.PositionExists(a1) {
			antinodes = append(antinodes, a1)
		} else {
			aDone = true
		}
		if !bDone && grid.PositionExists(a2) {
			antinodes = append(antinodes, a2)
		} else {
			bDone = true
		}

		i++
	}

	return antinodes
}

func GetBasicAntinodes(p1, p2 Position) (Position, Position) {
	diffX := p1.X - p2.X
	diffY := p1.Y - p2.Y

	a1 := Position{X: p1.X + diffX, Y: p1.Y + diffY}
	a2 := Position{X: p2.X - diffX, Y: p2.Y - diffY}

	return a1, a2
}

func partOne(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part one")

	grid := createGridFromString(dataString)
	antennas := grid.GetAntennas()

	unique_antinodes := make(map[Position]bool)
	for _, positions := range antennas {
		for i, p1 := range positions[:len(positions)-1] {
			for _, p2 := range positions[i+1:] {
				a1, a2 := GetBasicAntinodes(p1, p2)
				if grid.PositionExists(a1) {
					unique_antinodes[a1] = true
				}
				if grid.PositionExists(a2) {
					unique_antinodes[a2] = true
				}
			}
		}
	}

	for range unique_antinodes {
		result++
	}

	return
}

func partTwo(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part two")

	grid := createGridFromString(dataString)
	antennas := grid.GetAntennas()

	unique_antinodes := make(map[Position]bool)
	for _, positions := range antennas {
		for i, p1 := range positions[:len(positions)-1] {
			for _, p2 := range positions[i+1:] {
				for _, a := range GetAllAntinodes(p1, p2, grid) {
					unique_antinodes[a] = true
				}
			}
		}
	}

	for range unique_antinodes {
		result++
	}

	return
}

func main() {
	flag.Parse()

	var inputFile string
	if *isTest {
		inputFile = "input_test.txt"
		fmt.Println("Running 2024/8 solution on test input.")
	} else {
		inputFile = "input.txt"
		fmt.Println("Running 2024/8 solution on full input.")
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
