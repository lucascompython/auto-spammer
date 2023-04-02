// io.go
package main

import (
	"C"
	"encoding/json"
	"fmt"
	"runtime"
	"strconv"
	"strings"
	"time"

	"github.com/go-vgo/robotgo"
	hook "github.com/robotn/gohook"
)

var FKeysLinux = map[uint16]string{
	65470: "F1",
	65471: "F2",
	65472: "F3",
	65473: "F4",
	65474: "F5",
	65475: "F6",
	65476: "F7",
	65477: "F8",
	65478: "F9",
	65479: "F10",
	65480: "F11",
	65481: "F12",
}

var FKeysWindows = map[uint16]string{
	112: "F1",
	113: "F2",
	114: "F3",
	115: "F4",
	116: "F5",
	117: "F6",
	118: "F7",
	119: "F8",
	120: "F9",
	121: "F10",
	122: "F11",
	123: "F12",
}

type KeyBinds struct {
	Binds map[string]string
}

var quitAutoClicker = make(chan bool)

func autoclicker(delay uint16) {
	for {
		select {
		case <-quitAutoClicker:
			return
		default:
			robotgo.Click()
			time.Sleep(time.Duration(delay) * time.Millisecond)
		}
	}
}

//export startHook
func startHook(bindJson string) {

	var binds KeyBinds

	err := json.Unmarshal([]byte(bindJson), &binds)
	if err != nil {
		fmt.Println("ERROR: ", err)
		return
	}

	fmt.Println(binds)
	when := 0

	if runtime.GOOS == "linux" {
		when = hook.KeyDown
	} else if runtime.GOOS == "windows" {
		when = hook.KeyUp
	}
	isClicking := false

	hook.Register(uint8(when), nil, func(e hook.Event) {
		fkey := ""
		if runtime.GOOS == "linux" {
			fkey = FKeysLinux[e.Rawcode]
		} else if runtime.GOOS == "windows" {
			fkey = FKeysWindows[e.Rawcode]
		}
		for k, v := range binds.Binds {
			if k == fkey {
				if strings.HasPrefix(v, "autoclicker:") {
					splited := strings.Split(v, ":")
					delay := splited[1]
					isClicking = !isClicking

					uintDelay, err := strconv.ParseUint(delay, 10, 16)
					if err != nil {
						fmt.Println("ERROR: ", err)
						return
					} else {
						uintDelay := uint16(uintDelay)
						if isClicking {
							go autoclicker(uintDelay)
						} else {
							quitAutoClicker <- true
						}
					}

					continue
				}
				robotgo.TypeStr(v)
			}

		}
	})

	s := hook.Start()
	<-hook.Process(s)
}

//export endHook
func endHook() {
	hook.End()
}

func main() {}
