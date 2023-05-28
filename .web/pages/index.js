import { useEffect, useRef, useState } from "react"
import { useRouter } from "next/router"
import { connect, E, getRefValue, isTrue, preventDefault, refs, updateState, uploadFiles } from "/utils/state"
import "focus-visible/dist/focus-visible"
import { Center, HStack, SkeletonText, Stack, Text, useColorMode, VStack } from "@chakra-ui/react"
import NextHead from "next/head"



export default function Component() {
  const [state, setState] = useState({"is_hydrated": false, "key1": "dapzsajigfyjjgicrvbwjfbrljjjiecqftobrylipfmmdxlznvauwexkadnmbdso", "key2": "tyadwmwazfcbpjavpabxnsbguurglbkysprsamacoltxdlyieoycfreirsdefysz", "options": ["a", "b"], "events": [{"name": "state.hydrate"}], "files": []})
  const [result, setResult] = useState({"state": null, "events": [], "processing": false})
  const router = useRouter()
  const socket = useRef(null)
  const { isReady } = router
  const { colorMode, toggleColorMode } = useColorMode()
  const focusRef = useRef();
  
  const Event = (events, _e) => {
      preventDefault(_e);
      setState({
        ...state,
        events: [...state.events, ...events],
      })
  }

  const File = files => setState({
    ...state,
    files,
  })

  useEffect(()=>{
    if(!isReady) {
      return;
    }
    if (!socket.current) {
      connect(socket, state, setState, result, setResult, router, ['websocket', 'polling'])
    }
    const update = async () => {
      if (result.state != null){
        setState({
          ...result.state,
          events: [...state.events, ...result.events],
        })

        setResult({
          state: null,
          events: [],
          processing: false,
        })
      }

      await updateState(state, setState, result, setResult, router, socket.current)
    }
    if (focusRef.current)
      focusRef.current.focus();
    update()
  })
  useEffect(() => {
    const change_complete = () => Event([E('state.hydrate', {})])
    router.events.on('routeChangeComplete', change_complete)
    return () => {
      router.events.off('routeChangeComplete', change_complete)
    }
  }, [router])


  return (
    <Center sx={{"width": "100%"}}>
  <VStack sx={{"width": "100%"}}>
  <Text>
  {("1 is " + state.key1)}
</Text>
  <Text>
  {("2 is " + state.key2)}
</Text>
  <Stack sx={{"width": "55%"}}>
  <SkeletonText noOfLines={8}/>
</Stack>
  <HStack>
  <Text>
  {state.options}
</Text>
</HStack>
</VStack>
  <NextHead>
  <title>
  {`Pynecone App`}
</title>
  <meta content="A Pynecone app." name="description"/>
  <meta content="favicon.ico" property="og:image"/>
</NextHead>
</Center>
  )
}
