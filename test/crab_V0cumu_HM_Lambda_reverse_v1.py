from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

config = config()

config.General.requestName = 'PAHM0_Lambda_cumu_eff_reverse_v12_rsb'
config.General.workArea = 'CrabArea'
config.General.transferOutputs = True
config.General.transferLogs = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'qwcumu_pPb16_HM0_Lm_eff_v2.py'
config.Data.inputDataset = '/PAHighMultiplicity0/davidlw-RecoSkim2016_Pbp_V0Cascade_v1-97be9aa52ea60cba5455e64649c12464/USER'
config.JobType.inputFiles = ['Hijing_8TeV_dataBS.root']
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 20
config.Data.outLFNDirBase = '/store/group/phys_heavyions/qwang/cumu/'
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/HI/Cert_285952-286496_HI8TeV_PromptReco_Pbp_Collisions16_JSON_NoL1T.txt'
config.Data.publication = False
config.Data.useParent = True
config.Site.storageSite = 'T2_CH_CERN'
config.Site.ignoreGlobalBlacklist = True
config.Data.ignoreLocality = True
config.Site.whitelist = ['T2_CH_CERN']
#config.Data.allowNonValidInputDataset = True
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#
#
##### 1
##config.Data.inputDataset = '/PAHighMultiplicity1/davidlw-RecoSkim2016_Pbp_V0Cascade_v1-97be9aa52ea60cba5455e64649c12464/USER'
#config.General.requestName = 'PAHM1_Lambda_cumu_eff_reverse_v12'
config.JobType.psetName = 'qwcumu_pPb16_HM1_Lm_eff_v2.py'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#
#### 2
#config.Data.inputDataset = '/PAHighMultiplicity2/davidlw-RecoSkim2016_Pbp_V0Cascade_v1-97be9aa52ea60cba5455e64649c12464/USER'
#config.General.requestName = 'PAHM2_Lambda_cumu_eff_reverse_v12'
##try:
##        crabCommand('submit', config = config)
##except HTTPException as hte:
##        print "Failed submitting task: %s" % (hte.headers)
##except ClientException as cle:
##        print "Failed submitting task: %s" % (cle)
##
#
#
#
#### 3
#config.Data.inputDataset = '/PAHighMultiplicity3/davidlw-RecoSkim2016_Pbp_V0Cascade_v1-97be9aa52ea60cba5455e64649c12464/USER'
#config.General.requestName = 'PAHM3_Lambda_cumu_eff_reverse_v12'
##try:
##        crabCommand('submit', config = config)
##except HTTPException as hte:
##        print "Failed submitting task: %s" % (hte.headers)
##except ClientException as cle:
##        print "Failed submitting task: %s" % (cle)
##
#
#
#
#### 4
#config.Data.inputDataset = '/PAHighMultiplicity4/davidlw-RecoSkim2016_Pbp_V0Cascade_v1-97be9aa52ea60cba5455e64649c12464/USER'
#config.General.requestName = 'PAHM4_Lambda_cumu_eff_reverse_v12'
##try:
##        crabCommand('submit', config = config)
##except HTTPException as hte:
##        print "Failed submitting task: %s" % (hte.headers)
##except ClientException as cle:
##        print "Failed submitting task: %s" % (cle)
##
#
#
#### 5
#config.Data.inputDataset = '/PAHighMultiplicity5/davidlw-RecoSkim2016_Pbp_V0Cascade_v1-97be9aa52ea60cba5455e64649c12464/USER'
#config.General.requestName = 'PAHM5_Lambda_cumu_eff_reverse_v12'
##try:
##        crabCommand('submit', config = config)
##except HTTPException as hte:
##        print "Failed submitting task: %s" % (hte.headers)
##except ClientException as cle:
##        print "Failed submitting task: %s" % (cle)
##
#
#
### 6
config.Data.inputDataset = '/PAHighMultiplicity6/davidlw-RecoSkim2016_Pbp_V0Cascade_v1-97be9aa52ea60cba5455e64649c12464/USER'
config.General.requestName = 'PAHM6_Lambda_cumu_eff_reverse_v12_rsb'
config.Site.whitelist = ['T2_US_Vanderbilt']
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)




#### 7
#config.Data.inputDataset = '/PAHighMultiplicity7/davidlw-RecoSkim2016_Pbp_V0Cascade_v1-97be9aa52ea60cba5455e64649c12464/USER'
#config.General.requestName = 'PAHM7_Lambda_cumu_eff_reverse_v12_rsb'
#config.JobType.psetName = 'qwcumu_pPb16_HM7_Lm_eff_v2.py'
#config.Site.whitelist = ['T2_US_Vanderbilt']
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#
