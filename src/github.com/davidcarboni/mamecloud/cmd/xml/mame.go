package main

import (
	"fmt"
	"io"
	"log"
	"os"
	"os/exec"
)

func main() {
	cmd := exec.Command("mame", "-listxml")
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		log.Fatal(err)
	}
	if err := cmd.Start(); err != nil {
		log.Fatal(err)
	}
	xml, err := os.Create("gomame.xml")
	if err != nil {
		log.Fatal(err)
	}
	defer xml.Close()
	fmt.Println("Writing xml...")
	n, err := io.Copy(xml, stdout)
	if err != nil {
		log.Fatal(err)
	}
	if err := cmd.Wait(); err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Done: %v\n", n)
}
