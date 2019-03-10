package main

import (
	"fmt"
	"io"
	"log"
	"os"
	"os/exec"
	"time"
)

func main() {
	start := time.Now()
	fmt.Println("Listing Mame xml...")
	cmd := exec.Command("mame", "-listxml")
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		log.Fatal(err)
	}
	if err := cmd.Start(); err != nil {
		log.Fatal(err)
	}
	xml, err := os.Create("mame.xml")
	if err != nil {
		log.Fatal(err)
	}
	defer xml.Close()
	written, err := io.Copy(xml, stdout)
	if err != nil {
		log.Fatal(err)
	}
	if err := cmd.Wait(); err != nil {
		log.Fatal(err)
	}
	end := time.Now()
	elapsed := end.Sub(start)
	fmt.Printf("Done. Wrote %vM in %.0fs.\n", written/(1024*1024), elapsed.Seconds())
}
