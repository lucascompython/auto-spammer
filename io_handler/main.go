package main

import (
	"C"
	"encoding/json"
	"fmt"
	"runtime"
	"time"

	"github.com/go-vgo/robotgo"
	hook "github.com/robotn/gohook"
)
import (
	"strconv"
	"strings"
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
		fmt.Println("newClicker")
		select {
		case <-quitAutoClicker:
			return
		default:
			robotgo.Click()
			time.Sleep(time.Duration(delay) * time.Millisecond)
		}
	}
}

func main() {
	fmt.Println("START")

	bindJson := `{
				"binds": {
					"F6": "ola",
					"F7": "autoclicker:100"
				}
			}`
	var binds KeyBinds

	json.Unmarshal([]byte(bindJson), &binds)
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
					fmt.Println("F7 -> activating/deactivating auto clicker")

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
		//switch fkey {
		//case "F1":
		//fmt.Println("F1")
		//robotgo.TypeStr("f1")
		//case "F2":
		//fmt.Println("F2")
		//robotgo.TypeStr("f2")
		//case "F3":
		//fmt.Println("F3")
		//robotgo.TypeStr("f3")
		//case "F4":
		//fmt.Println("F4")
		//robotgo.TypeStr("f4")
		//case "F5":
		//fmt.Println("F5")
		//robotgo.TypeStr("f5")
		//case "F6":
		//fmt.Println("F6")
		//robotgo.TypeStr("f6")
		////robotgo.TypeStr("comi!\"#$%&//()=?¡¿*+")
		//case "F7":
		//fmt.Println("F7 -> activating auto clicker")
		//if autoClickerActive {
		//autoClickerActive = false
		//} else {
		//autoClickerActive = true
		//}
		//case "F8":
		//fmt.Println("F8")
		//robotgo.TypeStr("f8")
		//case "F9":
		//fmt.Println("F9")
		//robotgo.TypeStr("f9")
		//case "F10":
		//fmt.Println("F10")
		//robotgo.TypeStr("f10")
		//case "F11":
		//fmt.Println("F11")
		//robotgo.TypeStr("f11")
		//case "F12":
		//fmt.Println("F12")
		//robotgo.TypeStr("f12")
		//}

		//if e.Rawcode-65411 == 65 {
		//fmt.Println("f7")
		//robotgo.TypeStr("comi")
		//}
	})

	s := hook.Start()
	defer hook.End()
	<-hook.Process(s)

	//hook.Register(hook.KeyDown, []string{"l", "ctrl", "shift"}, func(e hook.Event) {
	//fmt.Println("You pressed CTRL + SHIFT + L!")
	//robotgo.TypeStr("comi!\"#$%&/()=?¡¿*+")
	//})

	//s := hook.Start()
	//defer hook.End()
	//<-hook.Process(s)

}

// export endHook
func endHook() {
	hook.End()
}
