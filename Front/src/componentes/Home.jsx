import { Header } from "./Header";
import { Body } from "./Body";
import { Footer } from "./Footer";


export function Home() {
    return <div className="container">
        <Header></Header>
        <Body></Body>
        <Footer></Footer>
    </div>
}