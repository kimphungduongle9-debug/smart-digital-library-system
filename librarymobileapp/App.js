import React from "react";
import { Provider as PaperProvider } from "react-native-paper";
import Home from "./screens/Home/Home";

export default function App() {
    return (
        <PaperProvider>
            <Home />
        </PaperProvider>
    );
}