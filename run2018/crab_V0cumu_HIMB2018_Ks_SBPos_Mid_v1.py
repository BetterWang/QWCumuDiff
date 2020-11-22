from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException

config = config()

config.General.requestName = 'HIMB4_V0Cumu_Ks_SBPos_Mid_v2'
config.General.workArea = 'CrabArea'
config.General.transferOutputs = True
config.General.transferLogs = False
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'qwcumu_PbPb18_V0_v2.py'
#config.JobType.maxJobRuntimeMin = 2500
config.JobType.inputFiles = ['MC_Full_BDT250_D4.KS.weights.xml']
config.JobType.pyCfgParams = ['part=KS', 'massRange=SBPos', 'rap=Mid']
config.Data.inputDataset = '/HIMinimumBias4/qwang-V0Skim_v3-9d53152409b8a9b6fb15042030d9bf69/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
#config.Data.unitsPerJob = 8
config.Data.outLFNDirBase = '/store/group/phys_heavyions/qwang/PbPb2018'
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/HI/PromptReco/Cert_326381-327564_HI_PromptReco_Collisions18_JSON.txt'
config.Data.publication = False
#config.Data.outputDatasetTag = ''
config.Data.useParent = True
config.Data.ignoreLocality = True
config.Site.whitelist = ['T2_US_Vanderbilt']
config.Site.storageSite = 'T2_CH_CERN'
config.Data.allowNonValidInputDataset = True
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)


config.JobType.psetName = 'qwcumu_PbPb18_V0_v2s.py'
#config.General.requestName = 'HIMB1_V0Cumu_Ks_SBPos_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias1/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#

config.Site.ignoreGlobalBlacklist = True
config.Data.splitting = 'Automatic'

#config.General.requestName = 'HIMB2_V0Cumu_Ks_SBPos_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias2/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.General.requestName = 'HIMB19_V0Cumu_Ks_SBPos_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias19/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.General.requestName = 'HIMB18_V0Cumu_Ks_SBPos_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias18/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.General.requestName = 'HIMB17_V0Cumu_Ks_SBPos_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias17/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.General.requestName = 'HIMB16_V0Cumu_Ks_SBPos_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias16/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.General.requestName = 'HIMB16_V0Cumu_Ks_SBPos1_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias16/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#config.JobType.pyCfgParams = ['part=KS', 'massRange=SBPos1', 'rap=Mid']
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.General.requestName = 'HIMB1_V0Cumu_Ks_SBPos1_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias1/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#config.JobType.pyCfgParams = ['part=KS', 'massRange=SBPos1', 'rap=Mid']
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.General.requestName = 'HIMB0_V0Cumu_Ks_SBPos1_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias0/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#config.JobType.pyCfgParams = ['part=KS', 'massRange=SBPos1', 'rap=Mid']
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.General.requestName = 'HIMB3_V0Cumu_Ks_SBPos1_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias3/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#config.JobType.pyCfgParams = ['part=KS', 'massRange=SBPos1', 'rap=Mid']
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.General.requestName = 'HIMB0_V0Cumu_Ks_SBPos_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias0/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.General.requestName = 'HIMB3_V0Cumu_Ks_SBPos_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias3/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.General.requestName = 'HIMB5_V0Cumu_Ks_SBPos_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias5/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.General.requestName = 'HIMB6_V0Cumu_Ks_SBPos_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias6/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.General.requestName = 'HIMB7_V0Cumu_Ks_SBPos_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias7/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.General.requestName = 'HIMB8_V0Cumu_Ks_SBPos_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias8/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.General.requestName = 'HIMB9_V0Cumu_Ks_SBPos_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias9/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.General.requestName = 'HIMB10_V0Cumu_Ks_SBPos_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias10/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#

config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 3

#config.General.requestName = 'HIMB11_V0Cumu_Ks_SBPos_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias11/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.General.requestName = 'HIMB12_V0Cumu_Ks_SBPos_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias12/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.General.requestName = 'HIMB13_V0Cumu_Ks_SBPos_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias13/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.General.requestName = 'HIMB14_V0Cumu_Ks_SBPos_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias14/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
#config.General.requestName = 'HIMB15_V0Cumu_Ks_SBPos_Mid_v2'
#config.Data.inputDataset = '/HIMinimumBias15/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
#try:
#        crabCommand('submit', config = config)
#except HTTPException as hte:
#        print "Failed submitting task: %s" % (hte.headers)
#except ClientException as cle:
#        print "Failed submitting task: %s" % (cle)
#
config.JobType.psetName = 'qwcumu_PbPb18_V0_noAPCut_v2s.py'
config.General.requestName = 'HIMB0_V0Cumu_Ks_SBPos_Mid_noAPCut_v2'
config.Data.inputDataset = '/HIMinimumBias0/qwang-V0Skim_v3-5f932986cf38f9e8dbd6c3aea7f6c2b4/USER'
try:
        crabCommand('submit', config = config)
except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
except ClientException as cle:
        print "Failed submitting task: %s" % (cle)

