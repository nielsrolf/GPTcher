import { Auth, ThemeSupa } from '@supabase/auth-ui-react'
import { useSession, useSupabaseClient } from '@supabase/auth-helpers-react'
import Menu from '../components/Menu'
import DemoCarousel from '@/components/DemoCarousel';
import { useEffect } from 'react'
import Starfield from '../components/Starfield';

const Home = () => {
  const session = useSession()
  const supabase = useSupabaseClient()

  return (
    <div>
      <Starfield />
      <div id='content-wide'>
        <Menu session={session} supabase={supabase} />
        <img src="/Logo_klein.svg" alt="GPTcher Logo" style={{float: 'left', width: '30vw'}} />
        <h1>GPTcher</h1>
        <h2>Hola I'm a language tutor bot</h2>
        <p>
          Learn by conversing with an AI teacher, do exercises, train your vocabulary and give us feedback! This project is in beta, so please be patient with us.
        </p>
        <DemoCarousel />
        <div id='content'>
          <iframe id="reddit-embed" src="https://www.redditmedia.com/r/learnspanish/comments/10l86bi/we_made_a_telegram_bot_that_teaches_you_spanish/j5vckiq/?depth=1&amp;showmore=false&amp;embed=true&amp;showmedia=false" sandbox="allow-scripts allow-same-origin allow-popups" style={{'border': 'none', 'width': '100%'}} scrolling="no"></iframe>
          <iframe id="reddit-embed" src="https://www.redditmedia.com/r/learnspanish/comments/10l86bi/we_made_a_telegram_bot_that_teaches_you_spanish/j5wqxuo/?depth=1&amp;showmore=false&amp;embed=true&amp;showmedia=false" sandbox="allow-scripts allow-same-origin allow-popups" style={{'border': 'none', 'width': '100%'}} height="139" width="640" scrolling="no"></iframe>
          <iframe id="reddit-embed" src="https://www.redditmedia.com/r/learnspanish/comments/10l86bi/we_made_a_telegram_bot_that_teaches_you_spanish/j5y70op/?depth=1&amp;showmore=false&amp;embed=true&amp;showmedia=false" sandbox="allow-scripts allow-same-origin allow-popups" style={{'border': 'none', 'width': '100%'}} height="218" width="640" scrolling="no"></iframe>
          <iframe id="reddit-embed" src="https://www.redditmedia.com/r/learnspanish/comments/10l86bi/we_made_a_telegram_bot_that_teaches_you_spanish/j5vurkh/?depth=1&amp;showmore=false&amp;embed=true&amp;showmedia=false" sandbox="allow-scripts allow-same-origin allow-popups" style={{'border': 'none', 'width': '100%'}} scrolling="no"></iframe>
          <iframe id="reddit-embed" src="https://www.redditmedia.com/r/learnspanish/comments/10l86bi/we_made_a_telegram_bot_that_teaches_you_spanish/j5vepxu/?depth=1&amp;showmore=false&amp;embed=true&amp;showmedia=false" sandbox="allow-scripts allow-same-origin allow-popups" style={{'border': 'none', 'width': '100%'}} height="139" width="640" scrolling="no"></iframe>
          <iframe id="reddit-embed" src="https://www.redditmedia.com/r/learnspanish/comments/10l86bi/we_made_a_telegram_bot_that_teaches_you_spanish/j5x360g/?depth=1&amp;showmore=false&amp;embed=true&amp;showmedia=false" sandbox="allow-scripts allow-same-origin allow-popups" style={{'border': 'none', 'width': '100%'}} height="139" width="640" scrolling="no"></iframe>
          <iframe id="reddit-embed" src="https://www.redditmedia.com/r/learnspanish/comments/10l86bi/we_made_a_telegram_bot_that_teaches_you_spanish/j5x1e68/?depth=1&amp;showmore=false&amp;embed=true&amp;showmedia=false" sandbox="allow-scripts allow-same-origin allow-popups" style={{'border': 'none', 'width': '100%'}} height="139" width="640" scrolling="no"></iframe>
          <iframe id="reddit-embed" src="https://www.redditmedia.com/r/learnspanish/comments/10l86bi/we_made_a_telegram_bot_that_teaches_you_spanish/j5xdouc/?depth=1&amp;showmore=false&amp;embed=true&amp;showmedia=false" sandbox="allow-scripts allow-same-origin allow-popups" style={{'border': 'none', 'width': '100%'}} height="139" width="640" scrolling="no"></iframe>
          <iframe id="reddit-embed" src="https://www.redditmedia.com/r/learnspanish/comments/10l86bi/we_made_a_telegram_bot_that_teaches_you_spanish/j5xqncd/?depth=1&amp;showmore=false&amp;embed=true&amp;showmedia=false" sandbox="allow-scripts allow-same-origin allow-popups" style={{'border': 'none', 'width': '100%'}} scrolling="no"></iframe>
          <iframe id="reddit-embed" src="https://www.redditmedia.com/r/learnspanish/comments/10l86bi/we_made_a_telegram_bot_that_teaches_you_spanish/j615n4q/?depth=1&amp;showmore=false&amp;embed=true&amp;showmedia=false" sandbox="allow-scripts allow-same-origin allow-popups" style={{'border': 'none', 'width': '100%'}} height="163" width="640" scrolling="no"></iframe>
          <iframe id="reddit-embed" src="https://www.redditmedia.com/r/learnspanish/comments/10l86bi/we_made_a_telegram_bot_that_teaches_you_spanish/j6hlbit/?depth=1&amp;showmore=false&amp;embed=true&amp;showmedia=false" sandbox="allow-scripts allow-same-origin allow-popups" style={{'border': 'none', 'width': '100%'}} height="139" width="640" scrolling="no"></iframe>
          <iframe id="reddit-embed" src="https://www.redditmedia.com/r/learnspanish/comments/10l86bi/we_made_a_telegram_bot_that_teaches_you_spanish/j5z1w3p/?depth=1&amp;showmore=false&amp;embed=true&amp;showmedia=false" sandbox="allow-scripts allow-same-origin allow-popups" style={{'border': 'none', 'width': '100%'}} height="139" width="640" scrolling="no"></iframe>
          <iframe id="reddit-embed" src="https://www.redditmedia.com/r/learnspanish/comments/10l86bi/we_made_a_telegram_bot_that_teaches_you_spanish/j7g0cmv/?depth=1&amp;showmore=false&amp;embed=true&amp;showmedia=false" sandbox="allow-scripts allow-same-origin allow-popups" style={{'border': 'none', 'width': '100%'}} height="223" width="640" scrolling="no"></iframe>
          <iframe id="reddit-embed" src="https://www.redditmedia.com/r/learnspanish/comments/10l86bi/we_made_a_telegram_bot_that_teaches_you_spanish/j7haze3/?depth=1&amp;showmore=false&amp;embed=true&amp;showmedia=false" sandbox="allow-scripts allow-same-origin allow-popups" style={{'border': 'none', 'width': '100%'}} height="139" width="640" scrolling="no"></iframe>
        </div>
      </div>
    </div>
  )
}

export default Home
