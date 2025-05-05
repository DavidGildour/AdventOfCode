// https://adventofcode.com/2024/day/12
package main

import (
	"errors"
	"flag"
	"fmt"
	"log"
	"os"
	"regexp"
	"slices"
	"sort"
	"strings"
	"time"
	"unicode"
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
	VOID = '\000'
)

// ##################### Position #####################

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

func (p Position) GetAllValidNeighbours(plotSet *PlotSet, plotType byte) (neighbours []Position) {
	for _, dir := range []Dir{N, E, W, S} {
		candidate := p.GetNeighbour(dir)
		isAvailable := plotSet.PlotIsAvailable(candidate, plotType)

		if isAvailable {
			neighbours = append(neighbours, candidate)
		}
	}

	return
}

func createPositionFromIndex(ix, rowLength int) Position {
	return Position{
		X: ix % rowLength,
		Y: ix / rowLength,
	}
}

// ##################### Plot #####################

type Plot struct {
	Pos  Position
	Type byte
}

func (p Plot) String() string {
	return fmt.Sprintf("%v: %v", string(p.Type), p.Pos)
}

// ##################### PlotSet #####################

type PlotSet map[Plot]struct{}

func (p *PlotSet) PopPlot() (Plot, error) {
	for k := range *p {
		p.RemovePlot(k)
		return k, nil
	}

	return Plot{}, errors.New("Empty set")
}

func (p *PlotSet) PlotIsAvailable(pos Position, plotType byte) bool {
	_, ok := (*p)[Plot{pos, plotType}]
	return ok
}

func (p *PlotSet) AddPlot(pos Position, plotType byte) {
	newPlot := Plot{pos, plotType}
	(*p)[newPlot] = struct{}{}
}

func (p *PlotSet) RemovePlot(plot Plot) {
	delete(*p, plot)
}

// ##################### Region #####################

type Region struct {
	Positions []Position
	Type      byte
}

func (r Region) GetAllPlots() *PlotSet {
	result := make(PlotSet)
	for _, pos := range r.Positions {
		result.AddPlot(pos, r.Type)
	}

	return &result
}

func (r Region) Area() int {
	return len(r.Positions)
}

func (r Region) Perimeter() (result int) {
	plotSet := r.GetAllPlots()

	for _, pos := range r.Positions {
		result += 4 - len(pos.GetAllValidNeighbours(plotSet, r.Type))
	}

	return
}

func (r Region) Sides() (sides int) {
	verticalSlices := make(map[int][]Position)
	horizontalSlices := make(map[int][]Position)
	for _, pos := range r.Positions {
		verticalSlices[pos.X] = append(verticalSlices[pos.X], pos)
		horizontalSlices[pos.Y] = append(horizontalSlices[pos.Y], pos)
	}

	for _, slice := range verticalSlices {
		sides += r.countSides(slice, VERTICAL)
	}
	for _, slice := range horizontalSlices {
		sides += r.countSides(slice, HORIZONTAL)
	}

	return
}

func (r Region) countSides(regionSlice []Position, sliceType Orientation) int {
	addToLastSlice := func(slices *[][]Position, v Position) {
		if len(*slices) == 0 {
			*slices = append(*slices, []Position{})
		}
		(*slices)[len(*slices)-1] = append((*slices)[len(*slices)-1], v)
	}

	var dirs []Dir
	var sortType Orientation
	if sliceType == VERTICAL {
		sortType = HORIZONTAL
		dirs = []Dir{W, E}
	} else {
		sortType = VERTICAL
		dirs = []Dir{N, S}
	}

	plotSet := r.GetAllPlots()
	var sidesA, sidesB [][]Position
	lastIndexA, lastIndexB := -1, -1
	for _, pos := range Sort(regionSlice, sortType) {
		var currentIndex int
		if sliceType == VERTICAL {
			currentIndex = pos.Y
		} else {
			currentIndex = pos.X
		}

		continuityBrokenA := lastIndexA >= 0 && lastIndexA != currentIndex-1
		continuityBrokenB := lastIndexB >= 0 && lastIndexB != currentIndex-1
		positionHasSideA := !plotSet.PlotIsAvailable(pos.GetNeighbour(dirs[0]), r.Type)
		positionHasSideB := !plotSet.PlotIsAvailable(pos.GetNeighbour(dirs[1]), r.Type)

		if positionHasSideA {
			if continuityBrokenA {
				sidesA = append(sidesA, []Position{})
			}
			addToLastSlice(&sidesA, pos)
			lastIndexA = currentIndex
		}

		if positionHasSideB {
			if continuityBrokenB {
				sidesB = append(sidesB, []Position{})
			}
			addToLastSlice(&sidesB, pos)
			lastIndexB = currentIndex
		}
	}

	return len(sidesA) + len(sidesB)
}

// ##################### Grid #####################

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

func (g Grid) GetAllPlots() *PlotSet {
	result := make(PlotSet)
	for i := range g.Data {
		pos := createPositionFromIndex(i, g.RowLength)
		plotType := g.GetValue(pos)
		newPlot := Plot{pos, plotType}
		result[newPlot] = struct{}{}
	}

	return &result
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
	rowLength := strings.IndexFunc(dataString, unicode.IsSpace)
	colLength := strings.Count(dataString, "\n") + 1

	re := regexp.MustCompile(`\s`)

	return Grid{
		Data:      re.ReplaceAllString(dataString, ""),
		RowLength: rowLength,
		ColLength: colLength,
	}
}

// ##################### Others #####################

type Orientation int

const (
	VERTICAL Orientation = iota
	HORIZONTAL
)

func Sort(positions []Position, how Orientation) []Position {
	result := slices.Clone(positions)
	sort.Slice(result, func(i, j int) bool {
		if how == VERTICAL {
			return result[i].X < result[j].X
		}
		return result[i].Y < result[j].Y
	})

	return result
}

func ParseRegion(startingPlot Plot, plotSet *PlotSet) Region {
	plotType := startingPlot.Type
	var accumulatedPlots []Position
	positionsToCheckFrom := []Position{startingPlot.Pos}

	for len(positionsToCheckFrom) > 0 {
		currentPos := positionsToCheckFrom[0]
		accumulatedPlots = append(accumulatedPlots, currentPos)
		positionsToCheckFrom = positionsToCheckFrom[1:]

		validNeighbours := currentPos.GetAllValidNeighbours(plotSet, plotType)
		for _, neighbour := range validNeighbours {
			plotSet.RemovePlot(Plot{neighbour, plotType})
		}
		positionsToCheckFrom = append(positionsToCheckFrom, validNeighbours...)
	}

	return Region{
		Positions: accumulatedPlots,
		Type:      plotType,
	}
}

func ParseRegions(g Grid) (regions []Region) {
	plotsLeft := g.GetAllPlots()

	for {
		currentPlot, err := plotsLeft.PopPlot()
		if err != nil {
			break
		}
		regions = append(regions, ParseRegion(currentPlot, plotsLeft))
	}

	return
}

func partOne(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part one")

	grid := createGridFromString(dataString)
	for _, region := range ParseRegions(grid) {
		result += region.Area() * region.Perimeter()
	}
	return
}

func partTwo(dataString string) (result int, err error) {
	defer timeTrack(time.Now(), "part two")

	grid := createGridFromString(dataString)
	for _, region := range ParseRegions(grid) {
		result += region.Area() * region.Sides()
	}
	return
}

func main() {
	flag.Parse()

	var inputFile string
	if *isTest {
		inputFile = "input_test.txt"
		fmt.Println("Running 2024/12 solution on test input.")
	} else {
		inputFile = "input.txt"
		fmt.Println("Running 2024/12 solution on full input.")
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
