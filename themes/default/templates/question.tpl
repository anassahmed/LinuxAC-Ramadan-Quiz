<div id="question">
	%if question == "answered":
		<div id="question_answered" class="box success">تم إجابة السؤال بنجاح.</div>
	%elif not question:
		<div id="no_question" class="box warn">لا توجد أسئلة متاحة، ربما لأنك أجبتَ سؤال اليوم فِعلًا.</div>
	%else:
	<div id="question_text" class="box normal">
		<p> {{question.question}} </p>
	</div><!-- #question_text -->
	<div id="question_options" class="box normal">
		<form id="question_options_form" name="question_options" method="POST" action="{{rq.script}}/answer">
			<input type="hidden" name="user_id" value="{{user_id}}" />
		%for i in question.options:
			<input type="radio" id="{{i.id}}" name="answer" value="{{i.id}}" />
			<label for="{{i.id}}">{{i.option}}</label>
			<br />
		%end
			<div id="send_answer" class="box" style="text-align: center;">
				<input type="submit" value="أرسل الإجابة" />
			</div><!-- #send_answer -->
		</form>
	</div><!-- #question_options -->
	%end
	<div id="invite" class="box success">
		<button id="invite_button" onClick="sendInvite()">ادعُ أصدقاءك وزوِّد فرصة فوزك</button>
	</div><!-- #invite --> 
</div><!-- #question -->