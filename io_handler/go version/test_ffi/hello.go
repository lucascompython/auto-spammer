// hello.go
package main

import "C"
import "fmt"

//export hello
func hello() {
	fmt.Println("Hello from Go!")
}

func main() {}
