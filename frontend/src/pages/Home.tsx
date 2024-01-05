import {Box, CssBaseline} from "@mui/material"
import PrimaryAppBar from "./template/PrimaryAppBar"

// same as function Home() {}
const Home = () => {

    return (
      <>
        <Box sx={{display: "flex"}}>
            <CssBaseline />
            <PrimaryAppBar />
            Home
        </Box>
      </>
    )
  }
  
export default Home  