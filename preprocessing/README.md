# Preprocessing Checklist

The following is a checklist of releases and ages that I need to preprocess. The subjects (sub-*) listed below are ones that have problems in the preprocessing pipeline. Most of the subjects have problems in the last stage of preprocessing, the saveresids stage, with exception: "Please check your data: There are no significant voxels." If the subject has a different error, I've listed it below. If the subject is crossed out, it means the T1 is so bad that I've rejected it.

## Matlab Preprocessing Exception

```matlab
Error using spm_spm_saveresids (line 831)
Please check your data: There are no significant voxels.
Error in aamod_modelestimate (line 52)
            spm_spm_saveresids(SPM);
Error in aa_feval (line 18)
            [a b]=feval(funcname,varargin{:});
Error in aa_feval_withindices (line 6)
        [aap,resp]=aa_feval(mfile_alias,aap,task,indices(1));
Error in aa_doprocessing_onetask (line 151)
            [aap,resp]=aa_feval_withindices(mfile_alias,aap,task,indices);
Error in aaq_localsingle/runall (line 16)
                aa_doprocessing_onetask(obj.aap,job.task,job.k,job.indices);
Error in aa_doprocessing (line 408)
        taskqueue.runall(dontcloseexistingworkers, false);
Error in aa_user_bpho (line 105)
aa_doprocessing(aap);
```

## Bad Subject List (Structural)

### Release 7 (61)

- [x] Age 5
  - sub-NDARBW525JHY
  - ~~sub-NDARER115FTJ~~
  - sub-NDARFC188VT4
  - ~~sub-NDARFJ651RMJ~~
  - sub-NDARGC099LDZ
  - ~~sub-NDARHG906MEZ~~
  - sub-NDARHN482HPM
  - ~~sub-NDARRF415CBE~~
  - sub-NDARUR872MP9
- [x] Age 6
  - sub-NDARAU840EUZ
  - ~~sub-NDARCB142ZPB~~
  - ~~sub-NDAREW074ZM2~~
  - sub-NDARGH425GB9
  - ~~sub-NDARPV595RWB~~
  - sub-NDARWT274EX1
- [x] Age 7
  - sub-NDARDN996CPF
  - sub-NDARDU566NUY
  - sub-NDARFD213GMJ
  - ~~sub-NDARHW467TA8~~
  - sub-NDARJK842BCN
  - sub-NDARJT172UE0
  - ~~sub-NDARNV983DET~~
  - ~~sub-NDARRG269ML2~~
  - ~~sub-NDARTK056HL3~~
- [x] Age 8
  - sub-NDAREA788ZAM
  - ~~sub-NDARFK262EKF~~
  - ~~sub-NDARHX252NVH~~
  - ~~sub-NDARMR134HUY~~
  - ~~sub-NDARTB300BN3~~
  - sub-NDARUP441BKK
  - sub-NDARWF259RB2
- [x] Age 9
  - sub-NDAREN999ERM
  - sub-NDARLH043YDK
  - ~~sub-NDARLY872ZXA~~
  - ~~sub-NDARTT867NWT~~
  - sub-NDARUY379PT5
  - ~~sub-NDARVJ468UZC~~
  - ~~sub-NDARVZ525AA0~~
  - sub-NDARYN474PEK
  - sub-NDARYN857XMX
- [x] Age 10
  - sub-NDARAB055BPR
  - ~~sub-NDARBE912PB0~~
  - ~~sub-NDAREB953UMY~~
  - sub-NDARGK442YHH
  - ~~sub-NDARJJ216EGT~~
  - ~~sub-NDARRN047XHC~~
  - sub-NDARTV119WJK
  - sub-NDARTW456RAG
  - ~~sub-NDARTY533VXQ~~
  - sub-NDARXK303DDB
- [x] Age 11
  - sub-NDARDZ440NGK
  - sub-NDARLV812JXX
  - sub-NDARNE800DCT
  - ~~sub-NDARWT694TXM~~
  - ~~sub-NDARYD958HAX~~
- [x] Age 12
  - ~~sub-NDARWW174PA5~~
  - sub-NDARXW276NXN
- [x] Age 13
  - ~~sub-NDARAA947ZG5~~
- [x] Age 14
  - ~~sub-NDARXB023AMW~~ (Has T2 file, not T1)
  - ~~sub-NDARNK064DXY~~
- [x] Age 15
  - sub-NDARUU991VRE (EXCEPTION: Input to SVD must not contain NaN or Inf.)
- [x] Age 16

### Release 8 (22)

- [x] Age 5
  - ~~sub-NDARFN854EJB~~
- [x] Age 6
  - ~~sub-NDARGZ116HTR~~
  - sub-NDARHC357HLP
  - ~~sub-NDARJW697MYZ~~
  - ~~sub-NDARWA570DNL~~
- [x] Age 7
  - sub-NDARCC824FCL
  - ~~sub-NDARCV628NRY~~
  - sub-NDARFP243NWY
  - ~~sub-NDARFZ990EFG~~
- [x] Age 8
  - ~~sub-NDARFD628UVZ~~
  - ~~sub-NDARGU067HT7~~
  - ~~sub-NDARKZ949UAL~~
  - ~~sub-NDARRU820CXW~~
  - ~~sub-NDARUX818MGE~~
  - ~~sub-NDARVE980WU5~~
- [x] Age 9
  - ~~sub-NDARAW247CCF~~ (i0->c null rank sX == 0)
  - sub-NDARMJ877UTP
  - sub-NDARUK025ZFT
- [x] Age 10
  - sub-NDAREB303XDC
  - sub-NDARRB561VCP
- [x] Age 11
  - ~~sub-NDARTE115TAE~~
- [x] Age 12
  - ~~sub-NDARMC694YF3~~
  - sub-NDARNC489BX5
  - sub-NDARZE389XF0
- [x] Age 13
- [x] Age 14
- [x] Age 15
  - ~~sub-NDARLU529MP7~~
- [x] Age 16

### Images

Good Subject

![Good Subject](../images/Other/Good%20Subject%20T1.png)

Bad Subject

![Bad Subject](../images/Other/Bad%20Subject%20T1.png)

## Bad Subject List (Functional)

### Release 7 (51)

- [x] Age 5
  - sub-NDARWG200CUE
- [x] Age 6
  - sub-NDARDP725ZVY
  - sub-NDARZV983XK9
  - sub-NDARNP423EJQ
  - sub-NDARTL084LYM
  - sub-NDARPG874CMG
  - sub-NDARAN524ZK6
  - sub-NDAREW074ZM2
  - sub-NDARTC177RN5
- [x] Age 7
  - sub-NDARNT113YX7
  - sub-NDARRM158VXD
  - sub-NDARVV926KLM
- [x] Age 8
  - sub-NDARFW038ZNE
  - sub-NDARMR134HUY
  - sub-NDARJV225EYT
  - sub-NDARPL479LHN
  - sub-NDARUF236HM7
  - sub-NDARNG968RB9
  - sub-NDARTV034RN2
  - sub-NDARMA598JTX
  - sub-NDARVV704MND
  - sub-NDARVY859ENR
  - sub-NDARHN078CDT
  - sub-NDARZV749GAP
  - sub-NDAREN151YXN
- [x] Age 9
  - sub-NDARDE319VD1
  - sub-NDARVJ468UZC
  - sub-NDARCN500KJG
  - sub-NDARER379GTP
  - sub-NDARLF484WJL
  - sub-NDARKD124UHN
  - sub-NDARLL572UP2
  - sub-NDARTE432ZRH
- [x] Age 10
  - sub-NDAREB953UMY
  - sub-NDARCH514JCT
  - sub-NDARNN745ZEK
  - sub-NDARVF544YP6
  - sub-NDARTY533VXQ
  - sub-NDARBL242L4H
  - sub-NDARRR622MYT
- [x] Age 11
  - sub-NDARJG494YDY
  - sub-NDARHZ476MJP
  - sub-NDARXE854EDK
  - sub-NDARRG536CVP
  - sub-NDARAR238RZ8
- [x] Age 12
  - sub-NDARYD666FL0
  - sub-NDARVN280JTN
  - sub-NDARCC340ER5
  - sub-NDARUC980NZ5
  - sub-NDARHT019ER6
- [x] Age 13
- [x] Age 14
- [x] Age 15
  - sub-NDARKT312RUD
- [x] Age 16

### Release 8 (25)

- [x] Age 5
  - sub-NDARLY030ZBG
- [x] Age 6
  - sub-NDARXH270TJ8
  - sub-NDARYC287UFV
  - sub-NDARWE130JMG
- [x] Age 7
  - sub-NDARDM119WB1
  - sub-NDARCA050RZL
  - sub-NDARGZ116HTR
  - sub-NDARDF560NND
  - sub-NDARZA034RW7
- [x] Age 8
  - sub-NDARVE980WU5
  - sub-NDARWK793VK4
  - sub-NDARXG035ZVM
  - sub-NDARFV725LGA
  - sub-NDARZH699ZET
  - sub-NDARTU407HDD
  - sub-NDARJR280FEJ
- [x] Age 9
  - sub-NDARAW247CCF
- [x] Age 10
  - sub-NDARJW072UJ3
  - sub-NDARPL406KX4
  - sub-NDARPT670LAY
  - sub-NDARAP912JK3
- [x] Age 11
  - sub-NDARRR735VMN
- [x] Age 12
  - sub-NDARLN749FML
- [x] Age 13
- [x] Age 14
- [x] Age 15
  - sub-NDARLL968KK1
- [x] Age 16
  - sub-NDARDW178AC6

### Images

Good Subject

![Good Subject](../images/Other/Good%20Subject%20BOLD.png)

Bad Subject

![Bad Subject](../images/Other/Bad%20Subject%20BOLD.png)
