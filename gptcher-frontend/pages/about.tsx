import { useSession, useSupabaseClient } from '@supabase/auth-helpers-react'
import Menu from '../components/Menu'
import Starfield from '../components/Starfield'

const About = () => {
  const session = useSession()
  const supabase = useSupabaseClient()

  return (
    <div>
      <Starfield />
      <div id="content-wide">
        <Menu session={session} supabase={supabase} />
        <img src="/Logo_klein.svg" alt="GPTcher Logo" style={{float: 'left', width: '30vw'}} />
        <h1>About GPTcher</h1>
        <p style={{'fontFamily': "Arial, Helvetica, sans-serif"}}>
          GPTcher is a language tutor bot that teaches languages by conversing with you.
          It is based on the GPT-3 language model by OpenAI and uses deepl to validate translations.
          In addition to the conversation mode, it also contains GPT generated exercises, analysis of your vocabulary and a feedback system (this is work in progress).
          The project is currently in beta, so please be patient with us.
        </p>
        <h2>GPTcher on Telegram</h2>
        <p  style={{'fontFamily': "Arial, Helvetica, sans-serif"}}>
          You can use GPTcher on Telegram by adding <a href="https://t.me/GPTcherbot">@GPTcherbot</a> to your contacts.
        </p>
        <h2>Impressum</h2>
        <p  style={{'fontFamily': "Arial, Helvetica, sans-serif"}}>
          This website is made and owned by <a href="https://github.com/nielsrolf/">Niels Rolf Warncke</a> and Alina Kaplon. <br />
          <ul>
            <li>Address: Weihergasse 17, 61231 Bad Nauheim</li>
            <li>Contact: niels@pollinations.ai</li>
          </ul>
        </p>
      </div>
    </div>
  )
}

export default About
