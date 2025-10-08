css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 15%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 85%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://imgs.search.brave.com/OwozJ6gedfrWDrAvhZ4A5shV1VWwP39FVHhsbt4HknE/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9jZG4t/aWNvbnMtcG5nLmZy/ZWVwaWsuY29tLzI1/Ni8xMzg4OS8xMzg4/OTE2MS5wbmc_c2Vt/dD1haXNfd2hpdGVf/bGFiZWw" style="height: 40x; width: 40px; border-radius: 100%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://imgs.search.brave.com/ppfHrzorpwKew4689uydkpWjCxR8cqA51T4rBrJ0M00/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9jZG4u/cGl4YWJheS5jb20v/cGhvdG8vMjAxOC8w/NC8xOC8xOC81Ni91/c2VyLTMzMzEyNTZf/MTI4MC5wbmc"  style="height: 40px; width: 40px; border-radius: 100%; object-fit: cover;">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
