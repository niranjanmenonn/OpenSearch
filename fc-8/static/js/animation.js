'use strict';
(function(){
    function e(b,a){
        let f=gsap.timeline({defaults:{ease:d},repeat:-1});
        gsap.set(b,{opacity:1-a/c.length,stroke:g(a/c.length)});
        f.to(b,{attr:{ry:`-=${a*2.3}`,rx:`+=${a*1.4}`},ease:h})
         .to(b,{attr:{ry:`+=${a*2.3}`,rx:`-=${a*1.4}`},ease:k})
         .to(b,{duration:1,rotation:-180,transformOrigin:"50% 50%"},0)
         .timeScale(.5)
    }
    
    gsap.config({trialWarn:!1});
    
    let l=document.querySelector("#mainSVG"),
        c=gsap.utils.toArray(".ell"),
        d=CustomEase.create("custom","M0,0 C0.2,0 0.432,0.147 0.507,0.374 0.59,0.629 0.822,1 1,1 "),
        k=CustomEase.create("custom","M0,0 C0.266,0.412 0.297,0.582 0.453,0.775 0.53,0.87 0.78,1 1,1 "),
        h=CustomEase.create("custom","M0,0 C0.594,0.062 0.79,0.698 1,1 "),
        m=MotionPathPlugin.getLength("#ai"),
        g=gsap.utils.interpolate(["#359EEE","#FFC43D","#EF476F","#03CEA4"]);
    
    gsap.set(l,{visibility:"visible"});
    
    c.forEach((b,a)=>{
        m && gsap.delayedCall(a/(c.length-1),e,[b,a+1])
    });
    
    gsap.to("#aiGrad",{
        duration:4,
        delay:.75,
        attr:{x1:"-=300",x2:"-=300"},
        scale:1.2,
        transformOrigin:"50% 50%",
        repeat:-1,
        ease:"none"
    });
    
    gsap.to("#ai",{
        duration:1,
        scale:1.1,
        transformOrigin:"50% 50%",
        repeat:-1,
        yoyo:!0,
        ease:d
    });
})();
