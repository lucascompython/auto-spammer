package main

import (
	"fmt"

	"C"

	"github.com/go-vgo/robotgo"
)
import (
	"time"

	hook "github.com/robotn/gohook"
)

func main() {
	robotgo.Sleep(1)
	//robotgo.TypeStr("hello world!")
	fmt.Println("start gang")
	//autoClickerActive := false
	////add(&autoClickerActive)
	//go func() {
	//for {
	//if autoClickerActive {
	//robotgo.Click()
	//}
	//}
	//}()

	//// robotgo.MouseSleep = 0
	//// robotgo.KeySleep = 0

	//hook.Register(hook.KeyDown, []string{"f7"}, func(e hook.Event) {
	////toggle mouse auto clicker
	//fmt.Println("toggle mouse auto clicker")
	//if autoClickerActive {
	//autoClickerActive = false
	//} else {
	//autoClickerActive = true
	//}

	//})
	//i := 0
	//hook.Register(hook.KeyDown, []string{"f7"}, func(e hook.Event) {
	////robotgo.TypeStr("gang")
	////robotgo.WriteAll("comi o caralho da tua mae ontem antes de dormir")
	////robotgo.KeyTap("v", "control")
	//fmt.Println("ESTA MERDA FOI CLICADA")
	//robotgo.TypeStr("comi o caralho da tua mae ontem antes de dormir")
	//time.Sleep(100 * time.Millisecond)

	//i++
	//if i == 20 {
	//hook.End()
	//}
	//})
	//s := hook.Start()
	//defer hook.End()
	//<-hook.Process(s)

	time.Sleep(100 * time.Millisecond)
	fmt.Println(robotgo.Version)
	evChan := hook.Start()
	defer hook.End()
	//keys := []string{robotgo.Num0, robotgo.F6, robotgo.KeyP, robotgo.KeyL}
	//i := 0
	for ev := range evChan {
		if ev.Kind == hook.KeyDown || ev.Kind == hook.KeyUp || ev.Kind == hook.KeyHold {
			fmt.Println("event", ev)
		}
		//for _, key := range keys {
		//if string(ev.Keychar) == key {
		//if i == 20 {
		//hook.End()
		//}
		////if key == "num0" {
		////robotgo.TypeStr("gang")
		////i++
		////continue
		////} else if key == "num1" {
		////robotgo.TypeStr("comi o caralho da tua mae ontem antes de dormir")
		////i++
		////continue
		////}
		//robotgo.TypeStr("caralho")
		//i++
		//}
	}
}
