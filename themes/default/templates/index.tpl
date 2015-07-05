<!DOCTYPE HTML>
<html>
	<head>
		<title>LinuxAC Ramadhan Quiz</title>
		<link rel="stylesheet" href="{{rq.script}}/_theme/style.css" type="text/css" />
	</head>
	<body dir="rtl">
		<div id="content">
			<div id="contentWrap">
				<h1><img id="header" src="{{rq.script}}/_theme/LinuxACHeader.jpg" alt="مسابقة مجتمع لينُكس العربي الرمضانيّة" /></h1>
				%if not is_authed:
					<p class="box success">مرحبًا بكم في مسابقة مجتمع لينُكس العربي الرمضانيَّة، سيتم تحويلكم للحصول على الصلاحيات المطلوبة للتطبيق.</p>
					<script type="text/javascript">
						top.location.href = "{{!auth_url}}";
					</script>
				%else:
					<div id="fb-root"></div>
					<script>
					  window.fbAsyncInit = function() {
					    FB.init({
					      appId      : '{{APP_ID}}', // App ID
					      status     : true, // check login status
					      cookie     : true, // enable cookies to allow the server to access the session
					      xfbml      : true  // parse XFBML
					    });
						  FB.Canvas.setAutoGrow();
					    // Additional initialization code here
					    
					  };
					  
					  // Load the SDK Asynchronously
					  (function(d){
					     var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
					     if (d.getElementById(id)) {return;}
					     js = d.createElement('script'); js.id = id; js.async = true;
					     js.src = "//connect.facebook.net/ar_AR/all.js";
					     ref.parentNode.insertBefore(js, ref);
					   }(document));
					   
					   function sendInvite() {
						  FB.ui({method: 'apprequests',
						    message: 'ادعُ أصدقاءك للمسابقة لتزوِّد فرصتك في الفوز.',
						  });
						}
					</script>
					%if not is_liked:
						%include like
					%else:
						%include question question=question, user_id = user.id, rq = rq
					%end
				%end
				<div id="footer" class="box normal" style="text-align: center;">
					<a href="http://www.linuxac.org" target="_blank">المجتمع</a> | 
					<a href="http://www.facebook.com/linuxac.org" target="_blank">صفحة الفيسبوك</a> |
					<a href="https://plus.google.com/112394922650393601673/posts" target="_blank">صفحة غوغل+</a> |
					<a href="http://twitter.com/linuxac_org" target="_blank">صفحة تويتر</a> | 
					<a href="http://identi.ca/linuxacorg" target="_blank">صفحة آيدنتكا</a>
				</div><!-- #footer -->
			</div><!-- #contentWrap -->
		</div><!-- #content -->
	</body>
</html>