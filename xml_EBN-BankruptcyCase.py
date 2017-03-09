name="DebtorInfoType"
base="nc:EntityType"
ref="BankruptcyDischargeDate"
ref="BankruptcyDismissalDate"
ref="BusinessTaxIdentification"

name="CaseCourtEventType"
base="nc:EntityType"
ref="CourtEventLocationText"
ref="j:CourtEventSchedule"
ref="CourtEventTypeCode"

name="BankruptcyCaseType"
base="bankruptcy:BankruptcyCaseType"
"AmendedNotice"
"BankruptcyFilingDate"
"DebtorInfo"
"BankruptcyConversionDate"
"BankruptcyObjectionDischargeDate"
"BankruptcyObjectionConfirmationDate"
"BankruptcyProofClaimDate"
"BankruptcyGovernmentProofClaimDate"
"BankruptcyPlan13Date"
"BankruptcyPlan12Date"
"BankruptcyPlan11Date"
"BankruptcyJointDebtorDismissalDate"
"BankruptcyMeansText"
"BankruptcyPreviousChapterStatute"
"CaseCourtEvent"
"ScheduleEvent"
"ScheduleDate"
"BankruptcyCaseDocketDate"
"BankruptcyCaseTerminatedDate"
"BankruptcyCaseReopenedDate"
"BankruptcyCaseReterminatedDate"
"BankruptcyCaseTerminatingTransactionDate"
"BankruptcyCaseCurrentEventDate"
"BankruptcyPlan11ConfirmationDate"
"BankruptcyPlan11DenialDate"
"BankruptcyPlan12ConfirmationDate"
"BankruptcyPlan12DenialDate"
"BankruptcyPlan13ConfirmationDate"
"BankruptcyPlan13DenialDate"
"BankruptcyTemporaryRestrainingOrderDate"
"BankruptcyDisclosureStatementDate"
"BankruptcyApproveDisclosureStatementDate"
"BankruptcyFirstMeetingHeldDate"
"BankruptcyFinalMeetingHeldDate"
"BankruptcyTrusteeFinalAssetReportDate"
"BankruptcyTrusteeFinalNoAssetReportDate"
"Bankruptcy12ReportDate"
"Bankruptcy13ReportDate"
"BankruptcyReaffirmationAgreementDate"
"BankruptcyReaffirmationHearingDate"
"BankruptcyAppointTrusteeDate"
"BankruptcyFinalDecreeDate"
"BankruptcyRecusalDate"
"BankruptcyOrderTransferCaseDate"
"BankruptcySummonsIssuedDate"
"BankruptcySummonsServiceExecutedDate"
"BankruptcyPreTrialOrderDate"
"BankruptcyTrialHeldDate"
"BankruptcyIncompleteFilingDueDate"
"BankruptcyPlan11DueDate"
"BankruptcyPlan12DueDate"
"BankruptcyPlan13DueDate"
"BankruptcyDisclosureStatementDueDate"
"BankruptcyBallotDueDate"
"BankruptcyObjectionToDisclosureDueDate"
"BankruptcyFinalReportDueDate"
"BankruptcyAnswerDueDate"
"BankruptcyAppellantAppealsDesignationDueDate"
"BankruptcyAppelleeAppealsDesignationDueDate"
"BankruptcyRecordOnAppealsTransmissionDueDate"
"BankruptcyDocketText"
"BankruptcyEventDocketText"
"BankruptcyLeadCaseChapterNumber"
"BankruptcyFormCodeText"
"BankruptcyFormCategory"
"BankruptcyFormNameText"
"BankruptcyNoticeShortNameText"
"BankruptcyShortTitle"
"CommentText"
"DocketID"
"NoticePageCount"
"DocketText"
"DocumentFilingDate"

name="EBNBatchType"
base="nc:DocumentType"
ref="corefiling:CoreFilingMessage"
"BankruptcyCase" type="BankruptcyCaseType" substitutionGroup="bankruptcy:BankruptcyCase">
"AmendedNotice"  #(default prefix is nc:)
"BankruptcyConversionDate"
"BankruptcyObjectionDischargeDate"
"BankruptcyObjectionConfirmationDate"
"BankruptcyProofClaimDate"
"BankruptcyGovernmentProofClaimDate"
"BankruptcyPlan13Date"
"BankruptcyPlan12Date"
"BankruptcyPlan11Date"
"BankruptcyDischargeDate"
"BankruptcyDismissalDate"
"BusinessTaxIdentification"
"BankruptcyJointDebtorDismissalDate"
"BankruptcyMeansText"
"BankruptcyPreviousChapterStatute" type="j:StatuteType">
"DebtorInfo" type="DebtorInfoType">
"BankruptcyFormCodeText"
"BankruptcyFormCategory"
"BankruptcyFormNameText"
"BankruptcyNoticeShortNameText"
"BankruptcyFilingDate"
"BankruptcyDocketText"
"BankruptcyEventDocketText"
"BankruptcyLeadCaseChapterNumber"
"CommentText"
"NoticePageCount"
"EBNBatch" type="EBNBatchType">
"BankruptcyCaseDocketDate"
"BankruptcyCaseTerminatedDate"
"BankruptcyCaseReopenedDate"
"BankruptcyCaseReterminatedDate"
"BankruptcyCaseTerminatingTransactionDate"
"BankruptcyCaseCurrentEventDate"
"BankruptcyPlan11ConfirmationDate"
"BankruptcyPlan11DenialDate"
"BankruptcyPlan12ConfirmationDate"
"BankruptcyPlan12DenialDate"
"BankruptcyPlan13ConfirmationDate"
"BankruptcyPlan13DenialDate"
"BankruptcyTemporaryRestrainingOrderDate"
"BankruptcyDisclosureStatementDate"
"BankruptcyApproveDisclosureStatementDate"
"BankruptcyFirstMeetingHeldDate"
"BankruptcyFinalMeetingHeldDate"
"BankruptcyTrusteeFinalAssetReportDate"
"BankruptcyTrusteeFinalNoAssetReportDate"
"Bankruptcy12ReportDate"
"Bankruptcy13ReportDate"
"BankruptcyReaffirmationAgreementDate"
"BankruptcyReaffirmationHearingDate"
"BankruptcyAppointTrusteeDate"
"BankruptcyFinalDecreeDate"
"BankruptcyRecusalDate"
"BankruptcyOrderTransferCaseDate"
"BankruptcySummonsIssuedDate"
"BankruptcySummonsServiceExecutedDate"
"BankruptcyPreTrialOrderDate"
"BankruptcyTrialHeldDate"
"BankruptcyIncompleteFilingDueDate"
"BankruptcyPlan11DueDate"
"BankruptcyPlan12DueDate"
"BankruptcyPlan13DueDate"
"BankruptcyDisclosureStatementDueDate"
"BankruptcyBallotDueDate"
"BankruptcyObjectionToDisclosureDueDate"
"BankruptcyFinalReportDueDate"
"BankruptcyAnswerDueDate"
"BankruptcyAppellantAppealsDesignationDueDate"
"BankruptcyAppelleeAppealsDesignationDueDate"
"BankruptcyRecordOnAppealsTransmissionDueDate"
"BankruptcyShortTitle"
"DocumentFilingDate"
"DocketID"
"DocketText"
"ScheduleDate"
"ScheduleEvent"
"CaseCourtEvent" type="CaseCourtEventType">
"CourtEventLocationText"
"CourtEventTypeCode"
