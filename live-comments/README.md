## Live Comments

### What are we building ?

This 👇🏻👇🏻

<img src="https://lh3.googleusercontent.com/d/1tXFJku7U4Sw90faGrCnnkZ-USaGzYjVc" width="400" height="500" alt="youtube live comments"/>


➡️ A live comments stream where a lot of people can comment simultaneously and view each other's comments (simply put - an open chat room)

Functionally, we need to have the following capabilities
- Capability for users to comment as many times as they want
- <wip>


[FE] -100x-> [Django POST /new-comment] --> [Q] --> [worker + analytical processing] --> [DB]

[FE] <-1x- [Listener/every 1 second + filter which ones to publish] <--[DB]


Version 1 : Functional system which handles incoming comments in huge volume and publishes it to the viewers

Version 2 : ++ Real Time ML system to filter out hateful and offensive comments and prevent them from getting published => Active censoring + Passive Censoring

Version 3 : ++ Rate Limit for preventing certain users from over-publishing in a certaiin time window



Django things:
- setup project
- startapp
- makemigrations + migrate
- superuser

### Challenges at scale
- identifying chokepoints
- preventing re-sending or missing messages
- context aware censoring
