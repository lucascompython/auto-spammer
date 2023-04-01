package main

import (
	"fmt"

	"C"

	"github.com/go-vgo/robotgo"
	hook "github.com/robotn/gohook"
)

func main() {
	//robotgo.Sleep(3)
	//robotgo.TypeStr("hello world!")
	fmt.Println("start")
	autoClickerActive := false
	//add(&autoClickerActive)
	go func() {
		for {
			if autoClickerActive {
				robotgo.Click()
			}
		}
	}()

	robotgo.MouseSleep = 0

	hook.Register(hook.KeyDown, []string{"l"}, func(e hook.Event) {
		//toggle mouse auto clicker
		fmt.Println("toggle mouse auto clicker")
		if autoClickerActive {
			autoClickerActive = false
		} else {
			autoClickerActive = true
		}

	})
	s := hook.Start()
	defer hook.End()
	<-hook.Process(s)

	//low()
}

func add(autoClickerActive *bool) {
	fmt.Println("--- Please press ctrl + shift + q to stop hook ---")
	hook.Register(hook.KeyDown, []string{"q", "ctrl", "shift"}, func(e hook.Event) {
		fmt.Println("ctrl-shift-q")
		hook.End()
	})

	fmt.Println("--- Please press w---")
	hook.Register(hook.KeyDown, []string{"p"}, func(e hook.Event) {
		robotgo.TypeStr("puta")
	})
	hook.Register(hook.KeyDown, []string{"l"}, func(e hook.Event) {
		//toggle mouse auto clicker
		fmt.Println("toggle mouse auto clicker")
		*autoClickerActive = !*autoClickerActive
		if *autoClickerActive {
			*autoClickerActive = false
		} else {
			*autoClickerActive = true
		}

	})

	s := hook.Start()
	<-hook.Process(s)
}

func start_auto_clicker(delay int) {
	robotgo.MouseSleep = delay
	for {
		robotgo.Click("left")
	}
}

func low() {
	evChan := hook.Start()
	defer hook.End()

	for ev := range evChan {
		fmt.Println("hook: ", ev)
	}
}
