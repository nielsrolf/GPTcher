import { useSession, useSupabaseClient } from '@supabase/auth-helpers-react'
import Menu from '../components/Menu'
import Starfield from '../components/Starfield';


const Donate = () => {
  const session = useSession()
  const supabase = useSupabaseClient()

  return (
    <div>
        <Starfield />
        <div id="content">
        <Menu session={session} supabase={supabase} />
        <h1>Donate</h1>
            <p>
                GPTcher uses GPT-3 from openai, so it costs us roughly 0.30$ per conversation. If you donate you help make it available to everyone and you make us very happy. Unless the community donates as much as it costs, we will have no other option than making it paid - which we don't want to do. In case it happens we will give some free credits to the people who donated.
            </p>
            <div className='button-container'><a href="https://www.patreon.com/user/about?u=55105539"><button className='big-button'>Donate</button></a></div>
        </div>
    </div>
  )
}

export default Donate
