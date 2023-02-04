import parse from 'html-react-parser';


const TeacherMessage = ({message}: Any) => {
    return (
        <div key={message.id} className='teacher-msg-outer'>
            <img src="/Logo_klein.svg" alt="GPTcher Logo" style={{float: 'left', width: '50px', padding: '5px'}} />
            <div key={message.id} className='message-container teacher-message'>
                <div>
                    {parse(message.text.replace('</b>', '</b><hr>'))}
                </div>
                {message.text_en && (
                    <>
                        <hr />
                        <div>
                            {parse(message.text_en.replace('</b>', '</b><hr>'))}
                        </div>
                    </>
                )}
            </div>
        </div>
    )
}

export default TeacherMessage;