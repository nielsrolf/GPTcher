import parse from 'html-react-parser';


const TeacherMessage = ({message}: Any) => {
    return (
        <div key={message.id} className='teacher-msg-outer'>
            <img src="/Icon_YOU.svg" alt="GPTcher Logo" style={{float: 'right', width: '50px', padding: '5px'}} />
            <div key={message.id} className='message-container student-message'>
                <div>
                    {parse(message.text.replace('</b>', '</b><hr>'))}
                </div>
                {message.text_translated && (
                    <>
                        <hr />
                        <div>
                            {parse(message.text_translated.replace('</b>', '</b><hr>'))}
                        </div>
                    </>
                )}
            </div>
        </div>
    )
}

export default TeacherMessage;