import React from 'react';
import parse from 'html-react-parser';


const StudentMessage = React.forwardRef<HTMLDivElement, { message: Any }>((props, ref) => {
    const { message } = props;
    return (
        <div key={message.id} className='teacher-msg-outer'>
            <img src="/Icon_YOU.svg" alt="GPTcher Logo" style={{float: 'right', width: '50px', padding: '5px'}} />
            <div key={message.id} className='message-container student-message' ref={ref}>
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
    );
});

export default StudentMessage;
