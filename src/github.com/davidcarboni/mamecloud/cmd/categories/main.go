package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"strings"
)

// Machine represents category information about a Mame emulated machine
type Machine struct {

	// Attributes
	Name      string `json:"name"`
	Working   string `json:"working"`
	Mature    string `json:"mature"`
	NotMature string `json:"not_mature"`

	// Categories
	Categories []string `json:"categories"`
}

var machines = make(map[string]Machine)

func main() {

	// Find working machines (according to genre_OWS.ini)
	parseWorking()

	// Mark up mature and not mature machines (according to mature.ini and not_mature.ini)
	parseMature()
	parseNotMature()
	diffMature()

	// Get categories (according to catlist.ini and gerre.ini)
	parseCategories()

	// De-duplicate categories listed in multiple ini files
	dedupe()

	// Output
	writeJson()
	fmt.Printf("Parsed a total of %v machines.\n", len(machines))
}

func parseWorking() {
	count := 0
	for category, names := range processCategoryIni("genre_OWS") {
		for _, name := range names {
			machine := getMachine(name)
			machine.Categories = append(machine.Categories, category)
			machine.Working = "yes"
			machines[name] = machine
			count++
		}
	}
	fmt.Printf("Parsed %v working machines.\n", count)
}

func parseMature() {
	count := 0
	for _, name := range processSingleIni("mature") {
		machine := getMachine(name)
		machine.Mature = "yes"
		machines[name] = machine
		count++
	}
	fmt.Printf("Parsed %v mature machines.\n", count)
}

func parseNotMature() {
	count := 0
	for _, name := range processSingleIni("not_mature") {
		machine := getMachine(name)
		machine.NotMature = "yes"
		machines[name] = machine
		count++
	}
	fmt.Printf("Parsed %v not-mature machines.\n", count)
}

func diffMature() {
	both := 0
	neither := 0
	for _, machine := range machines {
		if machine.Mature == "yes" && machine.NotMature == "yes" {
			both++
		}
		if machine.Mature == "no" && machine.NotMature == "no" {
			neither++
		}
	}
	if both > 0 {
		fmt.Printf("There are %v machines are marked as both mature and not mature.\n", both)
	}
	if neither > 0 {
		fmt.Printf("There are %v machines are marked as neither mature nor not mature.\n", neither)
	}
}

func parseCategories() {

	categoryIni := []string{
		"catlist",
		"genre",
	}

	for _, iniFile := range categoryIni {
		for category, names := range processCategoryIni(iniFile) {
			for _, name := range names {
				machine := getMachine(name)
				machine.Categories = append(machine.Categories, category)
				machines[name] = machine
			}
		}
	}

}

func processSingleIni(iniFile string) []string {

	// Return value
	games := make([]string, 0)

	// Open the file
	ini, err := os.Open("catver/UI_files/" + iniFile + ".ini")
	if err != nil {
		log.Fatal(fmt.Sprintf("Error opening file: %v", iniFile), err)
	}
	defer ini.Close()

	// Parse the file
	processing := false
	scanner := bufio.NewScanner(ini)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())

		if strings.HasPrefix(line, "[") {

			// A category
			section := strings.Trim(line, "[]")
			processing = section == "ROOT_FOLDER"

		} else if processing && len(line) > 0 {

			// Game entry
			games = append(games, line)
		}

	}

	// Check for errors
	if err := scanner.Err(); err != nil {
		log.Fatal(fmt.Sprintf("Error parsing file: %v", iniFile), err)
	}

	return games
}

func processCategoryIni(iniFile string) map[string][]string {

	// Return value
	games := make(map[string][]string)

	// Open the file
	ini, err := os.Open("catver/UI_files/" + iniFile + ".ini")
	if err != nil {
		log.Fatal(fmt.Sprintf("Error opening file: %v", iniFile), err)
	}
	defer ini.Close()

	// Parse the file
	processing := false
	var category string
	scanner := bufio.NewScanner(ini)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())

		if strings.HasPrefix(line, "[") {

			// A category
			category = strings.Trim(line, "[]")
			processing = category != "FOLDER_SETTINGS" && category != "ROOT_FOLDER"

		} else if processing && len(line) > 0 {

			// Game entry
			games[category] = append(games[category], line)

		}
		//else if len(line) > 0 {
		//	fmt.Printf("Ignoring line: %s\n", line)
		//}

	}

	// Check for errors
	if err := scanner.Err(); err != nil {
		log.Fatal(fmt.Sprintf("Error parsing file: %v", iniFile), err)
	}

	return games
}

func getMachine(name string) Machine {
	machine, exists := machines[name]
	if !exists {
		machine = Machine{
			Name:       name,
			Working:    "no",
			Mature:     "no",
			NotMature:  "no",
			Categories: make([]string, 0),
		}
		machines[name] = machine
	}
	return machine
}

func dedupe() {
	for name, machine := range machines {
		machine.Categories = list(set(machine.Categories))
		machines[name] = machine
	}
}

func set(categoryList []string) map[string]bool {
	categorySet := make(map[string]bool)
	for _, category := range categoryList {
		categorySet[category] = true
	}
	return categorySet
}

func list(categorySet map[string]bool) []string {
	categoryList := make([]string, 0)
	for category := range categorySet {
		categoryList = append(categoryList, category)
	}
	return categoryList
}

func writeJson() {

	fmt.Println("Marshalling json...")
	jsonData, _ := json.MarshalIndent(machines, "", "  ")

	fmt.Println("Writing json...")
	jsonFile, err := os.Create("categories.json")
	if err != nil {
		log.Fatal("Error creating file:", err)
	}
	defer jsonFile.Close()

	if _, err := jsonFile.Write(jsonData); err != nil {
		log.Fatal("Error writing Json:", err)
	}
}
