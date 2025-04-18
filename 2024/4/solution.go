// https://adventofcode.com/2024/day/4
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
	NIL Dir = iota
	N
	NE
	E
	SE
	S
	SW
	W
	NW
)

type Grid struct {
	Data string
	RowLength int
	ColLength int
}

func (g Grid) GetValueIfExists(pos Position) byte {
	if g.PositionExists(pos) {
		return g.Data[pos.ToIndex(g.RowLength)]
	}

	return byte('\000')
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

func createGridFromString(dataString string) Grid {
	rowLength := strings.Index(dataString, "\n") - 1
	colLength := strings.Count(dataString, "\n") + 1

	re := regexp.MustCompile(`\W`)

	return Grid{
		Data: re.ReplaceAllString(dataString, ""),
		RowLength: rowLength,
		ColLength: colLength,
	}
}

type Position struct {
	X int
	Y int
}

func (p Position) ToIndex(rowLength int) int {
	return (p.Y*rowLength) + p.X
}

func (p Position) GetNeighbour(dir Dir) Position {
	switch dir {
	case N:
		return Position{p.X, p.Y - 1}
	case NE:
		return Position{p.X + 1, p.Y - 1}
	case E:
		return Position{p.X + 1, p.Y}
	case SE:
		return Position{p.X + 1, p.Y + 1}
	case S:
		return Position{p.X, p.Y + 1}
	case SW:
		return Position{p.X -1, p.Y + 1}
	case W:
		return Position{p.X - 1, p.Y}
	case NW:
		return Position{p.X - 1, p.Y -1}
	default:
		panic(fmt.Sprintf("Invalid direction: %v", dir))
	}
}

func (p Position) GetValidNeighbours(grid Grid) (map[Dir]Position) {
	res := make(map[Dir]Position)
	for _, dir := range []Dir{N, NE, E, SE, S, SW, W, NW} {
		neighbour := p.GetNeighbour(dir)
		if grid.PositionExists(neighbour) {
			res[dir] = neighbour
		}
	}

	return res
}

func createPositionFromIndex(ix, rowLength int) Position {
	return Position{
		X: ix % rowLength,
		Y: ix / rowLength,
	}
}


func searchWord(grid Grid, pos Position, dir Dir, remainingLetters string) (count int) {
	if len(remainingLetters) == 0 {
		return count + 1
	}

	wantedLetter := remainingLetters[0]

	if dir != NIL {
		next_pos := pos.GetNeighbour(dir)
		if grid.GetValueIfExists(next_pos) == wantedLetter {
			count += searchWord(grid, next_pos, dir, remainingLetters[1:])
		}
	} else {
		for newDir, neighbour := range pos.GetValidNeighbours(grid) {
			if grid.GetValue(neighbour) == wantedLetter {
				count += searchWord(grid, neighbour, newDir, remainingLetters[1:])
			}
		}
	}

	return
}

func countWordsFrom(grid Grid, pos Position) int {
	return searchWord(grid, pos, NIL, "MAS")
}

func spellsMAS(bytes []byte) bool {
	return string(bytes) == "MAS" || string(bytes) == "SAM"
}

func isValidXMAS(grid Grid, pos Position) int {
	topLeft := grid.GetValueIfExists(pos.GetNeighbour(NW))
	topRight := grid.GetValueIfExists(pos.GetNeighbour(NE))
	bottomLeft := grid.GetValueIfExists(pos.GetNeighbour(SW))
	bottomRight := grid.GetValueIfExists(pos.GetNeighbour(SE))

	if spellsMAS([]byte{topLeft, 'A', bottomRight}) && spellsMAS([]byte{bottomLeft, 'A', topRight}) {
		return 1
	}
	return 0
}

func partOne(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part one")

	grid := createGridFromString(dataString)
	positions := grid.get2DPositions('X', 0)

	for _, pos := range positions {
		result += countWordsFrom(grid, pos)
	}


	return
}

func partTwo(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part two")

	grid := createGridFromString(dataString)
	positions := grid.get2DPositions('A', 0)

	for _, pos := range positions {
		result += isValidXMAS(grid, pos)
	}


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
