          if( !is_data() && (applytriggerweight||skim_isFastsim)) {
    	         if(abs(lep1_pdgid()) == 11){ 
                   if(lep1_p4().pt()<500) triglep1*= h_trig_el->GetBinContent(h_trig_el->FindBin(lep1_p4().pt()));		
                   else  triglep1*= h_trig_el->GetBinContent(h_trig_el->FindBin(400));
                 }
    	         if(abs(lep1_pdgid()) == 13){
                   if(abs(lep1_p4().eta()) < 1.2) {
                   if(lep1_p4().pt()<500) triglep1*= h_trig_mu_eb->GetBinContent(h_trig_mu_eb->FindBin(lep1_p4().pt()));		
                   else  triglep1*= h_trig_mu_eb->GetBinContent(h_trig_mu_eb->FindBin(400));
                   }
                   else {
                   if(lep1_p4().pt()<500) triglep1*= h_trig_mu_ee->GetBinContent(h_trig_mu_ee->FindBin(lep1_p4().pt()));		
                   else  triglep1*= h_trig_mu_ee->GetBinContent(h_trig_mu_ee->FindBin(400));
                   }
                 }
            // lep2 is good electron
    	         if(abs(lep2_pdgid()) == 11 && lep2type()==1) {
                 if(abs(lep2_p4().eta()) < 1.442) {
                    if(lep2_p4().pt()<500) triglep2*= h_trig_el->GetBinContent(h_trig_el->FindBin(lep2_p4().pt()));		
                    else triglep2 *= h_trig_el->GetBinContent(h_trig_el->FindBin(400));
                 }
                 else {
                    if(lep2_p4().pt()<500) triglep2*= h_trig_el_ee->GetBinContent(h_trig_el_ee->FindBin(lep2_p4().pt()));		
                    else triglep2 *= h_trig_el_ee->GetBinContent(h_trig_el_ee->FindBin(400));
                   }
                }
            // lep2 is a veto electron`
    	         if(abs(lep2_pdgid()) == 11 && lep2type()==2) {
                 if(abs(lep2_p4().eta()) < 1.442) {
                    if(lep2_p4().pt()<500) triglep2*= h_trig_el_eb_veto->GetBinContent(h_trig_el_eb_veto->FindBin(lep2_p4().pt()));		
                    else triglep2 *= h_trig_el_eb_veto->GetBinContent(h_trig_el_eb_veto->FindBin(400));
                 }
                 else {
                    if(lep2_p4().pt()<500) triglep2*= h_trig_el_ee_veto->GetBinContent(h_trig_el_ee_veto->FindBin(lep2_p4().pt()));		
                    else triglep2 *= h_trig_el_ee_veto->GetBinContent(h_trig_el_ee_veto->FindBin(400));
                   }
                }
            // lep2 is good muon
    	         if(abs(lep2_pdgid()) == 13 && lep2type()==1){
                   if(abs(lep2_p4().eta()) < 1.2) {
                   if(lep2_p4().pt()<500) triglep2*= h_trig_mu_eb->GetBinContent(h_trig_mu_eb->FindBin(lep2_p4().pt()));		
                   else  triglep2*= h_trig_mu_eb->GetBinContent(h_trig_mu_eb->FindBin(400));
                   }
                   else {
                   if(lep2_p4().pt()<500) triglep2*= h_trig_mu_ee->GetBinContent(h_trig_mu_ee->FindBin(lep2_p4().pt()));		
                   else  triglep2*= h_trig_mu_ee->GetBinContent(h_trig_mu_ee->FindBin(400));
                   }
                 }
            // lep2 is veto muon
    	         if(abs(lep2_pdgid()) == 13 && lep2type()==2){
                   if(abs(lep2_p4().eta()) < 1.2) {
                   if(lep2_p4().pt()<500) triglep2*= h_trig_mu_eb_veto->GetBinContent(h_trig_mu_eb_veto->FindBin(lep2_p4().pt()));		
                   else  triglep2*= h_trig_mu_eb_veto->GetBinContent(h_trig_mu_eb_veto->FindBin(400));
                   }
                   else {
                   if(lep2_p4().pt()<500) triglep2*= h_trig_mu_ee_veto->GetBinContent(h_trig_mu_ee_veto->FindBin(lep2_p4().pt()));		
                   else  triglep2*= h_trig_mu_ee_veto->GetBinContent(h_trig_mu_ee_veto->FindBin(400));
                   }
                 }

               if(TString(selection).Contains("2lCR")) trigeff = 1-(1-triglep1)*(1-triglep2) ; else trigeff = triglep1;
                weight*= trigeff;
          }